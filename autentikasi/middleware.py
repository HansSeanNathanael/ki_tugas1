from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect

class HarusLogin:
    def __init__(self, get_response):
        self.get_response = get_response
        self.paths = [
            '/auth/tes/'
        ]

    def __call__(self, request : HttpRequest) -> HttpResponse:
        
        if request.path not in self.paths:
            return self.get_response(request)
        
        if request.user.is_authenticated:
            return self.get_response(request)
        return HttpResponseRedirect("/auth/login/")
        
        