from django import forms
from .models import Category, Subcategory
from django.db.models import Count

# 카테고리 선택 폼
class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.category + ' ({})'.format(obj.counter)

# 상품 입력 폼
class ProductRegisterForm(forms.Form):
    name = forms.CharField(
        error_messages={'required': '상품명을 입력해주세요.'},
        max_length=64, 
        label='상품명'
    )
    price = forms.IntegerField(
        error_messages={'required': '상품가격을 입력해주세요.'}, 
        label='상품가격'
    )
    description = forms.CharField(
        error_messages={'required': '상품설명을 입력해주세요.'}, 
        label='상품설명'
    )
    stock = forms.IntegerField(
        error_messages={'required': '재고를 입력해주세요.'}, 
        label='재고'
    )
    thumbnail_image = forms.ImageField(
        error_messages={'required': '썸네일 이미지를 입력해주세요.'}, 
        label='썸네일 이미지'
    )
    images = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'multiple': True, 'class':'adjasfkajsdklj'}
        ),
        label='여러 개의 이미지'
    )   
    category = CategoryChoiceField(
        queryset = Category.objects.all().annotate(counter=Count('category')),
        error_messages={'required': '카테고리를 입력해주세요.'}, 
        label = '카테고리'
    )
    subcategory = CategoryChoiceField(
        queryset = Subcategory.objects.all().annotate(counter=Count('category')),
        error_messages={'required': '세부 카테고리를 입력해주세요.'}, 
        label = '세부 카테고리'
    )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        description = cleaned_data.get('description')
        stock = cleaned_data.get('stock')
        image = cleaned_data.get('image')

        if not (name and price and description and stock and image):
            self.add_error('name', '값이 없습니다')
            self.add_error('price', '값이 없습니다')