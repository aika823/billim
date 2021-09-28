from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', )

    def changelist_view(self, request, extra_context=None):
        extra_context = { 'title': '사용자 목록' }
        return super().changelist_view(request, extra_context)
 
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        user = User.objects.get(pk=object_id)
        extra_context = { 'title': f'{user.email} 수정하기' }
        return super().changeform_view(request, object_id, form_url, extra_context)       


admin.site.register(User, UserAdmin)
admin.site.site_header = '패스트캠퍼스'
admin.site.index_title = '패스트캠퍼스'
admin.site.site_title = '패스트캠퍼스'
