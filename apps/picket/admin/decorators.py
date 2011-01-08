from django.conf import settings
from django.contrib.messages import error
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _


def role_required(role):
    
    def decorator(func):
        
        def wrapper(request, *args, **kwargs):
            
            def test():
                return request.user.is_superuser or {
                    'manager': bool(request.my_projects),
                    'head': bool(request.my_departments),
                }.get(role, False)
            
            if test():
                return func(request, *args, **kwargs)
            else:
                error(request, _('Permission denied'))
                return redirect(settings.LOGIN_URL)
        
        return wrapper
    
    return decorator
