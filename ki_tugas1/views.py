from django.http.request import HttpRequest
from django.core.exceptions import BadRequest
from django.views import View

class Views(View):
    
    def invoke(self, request : HttpRequest, *args, **kwargs):
        try:
            return getattr(self, request.method.lower())(request, args, kwargs)
        except AttributeError:
            return BadRequest('Method not supported.')
