from django import forms
from .models import Seller

class RegisterForm(forms.Form):
    name = forms.CharField(
        error_messages={'required': '이름을 입력해주세요.'},
        max_length=64, 
        label='셀러 이름 (상호명)'
    )
    address = forms.CharField(
        max_length=64,
        error_messages={'required': '주소를 입력해주세요.'}, 
        label='주소'
    )
    address_detail = forms.CharField(
        max_length=64,
        error_messages={'required': '상세주소를 입력해주세요.'}, 
        label='상세주소'
    )
    phone_number = forms.CharField(
        max_length=64,
        error_messages={'required': '전화번호를 입력해주세요.'}, 
        label='전화번호'
    )
    mobile_number = forms.CharField(
        max_length=64,
        error_messages={'required': '휴대전화 번호를 입력해주세요.'}, 
        label='휴대전화 번호'
    )
    image = forms.ImageField(
        error_messages={'required': '셀러 이미지를 입력해주세요.'}, 
        label='셀러 이미지'
    )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        address = cleaned_data.get('address')
        address_detail = cleaned_data.get('address_detail')
        phone_number = cleaned_data.get('phone_number')
        mobile_numer = cleaned_data.get('mobile_number')
        image = cleaned_data.get('image')