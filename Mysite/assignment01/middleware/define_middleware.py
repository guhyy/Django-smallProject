from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,HttpResponse,redirect

class check_session(MiddlewareMixin):
    def process_request(self,request):
        if request.path_info == '/login/':
            return 
        info = request.session.get('info')
        if not info:
            return redirect('/login/')
        return 
    def process_response(self,request,response): 
        return response