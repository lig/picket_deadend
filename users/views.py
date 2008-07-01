"""
Copyright 2008 Serge Matveenko

This file is part of Picket.

Picket is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Picket.  If not, see <http://www.gnu.org/licenses/>.
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User
from django.http                    import HttpResponseRedirect
from django.shortcuts     import get_object_or_404, render_to_response
from django.template                import RequestContext
from django.utils.translation       import ugettext as _

from users.forms    import ProfileForm
from users.models   import BASE_URL, Profile

def user(req, username):
    
    user = get_object_or_404(User, username=username)
    
    try:
        profile = user.get_profile()
    except Profile.DoesNotExist:
        if user == req.user:
            return HttpResponseRedirect(
                '%sprofile/' % user.get_absolute_url())
        else:
            profile = None
    
    return render_to_response('users/user.html',
        {'cur_user': user, 'cur_profile': profile,},
        context_instance=RequestContext(req))

@login_required
def profile(req, username):
    
    user = get_object_or_404(User, username=username, id=req.user.id)
        
    profile, created = Profile.objects.get_or_create(user=user,
        defaults={'phone': '',})
    
    if 'POST' == req.method:
        profileForm = ProfileForm(req.POST, instance=profile)
        if profileForm.is_valid():
            profile = profileForm.save()
            user.message_set.create(
                message=_('your profile is updated'))
            return HttpResponseRedirect(user.get_absolute_url())
    else:
        profileForm = ProfileForm(instance=profile)
    
    return render_to_response('users/profile.html',
        {'profile_form': profileForm,},
        context_instance=RequestContext(req))
