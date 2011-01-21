from django.conf import settings
from django.contrib.messages import error
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from ..documents import Project, Department

def role_required(role):
    
    def decorator(func):
        
        def wrapper(request, *args, **kwargs):
            
            def test():
                return bool(request.user.is_superuser or {
                    'manager': request.my_projects and
                        kwargs.get('project_id') and
                        Project.objects.filter(pk=kwargs['project_id'] #@UndefinedVariable
                            ).first() in request.my_projects, #@UndefinedVariable
                    'head': request.my_departments and
                        kwargs.get('department_id') and
                        Department.objects.filter(pk=kwargs['department_id'] #@UndefinedVariable
                            ).first() in request.my_departments, #@UndefinedVariable
                }.get(role))
            
            if test():
                return func(request, *args, **kwargs)
            else:
                error(request, _('Permission denied'))
                return redirect(settings.LOGIN_URL)
        
        return wrapper
    
    return decorator
