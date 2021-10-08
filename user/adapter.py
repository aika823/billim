from django.conf import settings
from django.shortcuts import redirect, render
import requests
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        code = request.GET.get('code')
        url_auth = 'https://oauth2.googleapis.com/token'
        client_id = '1094555666329-b76moi8dkckmoe3vc9kb2qhf60r8t563.apps.googleusercontent.com'
        client_secret = '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'
        data = {
            "grant_type":'authorization_code',
            'client_id':client_id,
            'client_secret':client_secret,
            'redirect_uri':'http://localhost:8000',
            'code':str(code),
        }
        response = requests.request("POST",url_auth,data=data)
        print(response.text)

        path = "/user/callback/google"
        return path.format()