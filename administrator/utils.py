from django.http.response import Http404, HttpResponseBadRequest

def administrator_required(function):
    
    def __inner__(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_administrator:
            return function(request, *args, **kwargs)
        return HttpResponseBadRequest("Only administrators allowed")
    return __inner__
        