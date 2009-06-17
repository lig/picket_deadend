from django.contrib.sites.models import Site

def navi(request):
    
    return {'site': Site.objects.get_current(),}
