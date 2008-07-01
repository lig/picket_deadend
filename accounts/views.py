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

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from accounts.forms import RegForm, ValForm, PassForm
from accounts.models import Validator

def registration(req):
    if req.user.is_authenticated():
        return HttpResponseRedirect(req.user.get_absolute_url())
    elif 'POST'==req.method:
        regForm = RegForm(req.POST)
        if regForm.is_valid():
            newUser = User.objects.create_user(regForm.cleaned_data['username'],
                regForm.cleaned_data['email'])
            newUser.first_name, newUser.last_name = regForm.cleaned_data['first_name'], regForm.cleaned_data['last_name']
            newUser.is_active = False
            validator = Validator(user=newUser)
            validator.save()
            newUser.email_user(_('New account email confirmation'),
                render_to_string('registration/checkemail.eml',
                    {'newUser': newUser, 'newUser_email': newUser.email,
                        'valCode': validator.code},
                    context_instance=RequestContext(req)))
            newUser.set_password(validator.code)
            newUser.save()
            return HttpResponseRedirect('/accounts/validation/')
    else:
        regForm = RegForm()
    return render_to_response('registration/signup.html', {'regForm': regForm},
        context_instance=RequestContext(req))

def validation(req):
    if req.user.is_authenticated():
        return HttpResponseRedirect(req.user.get_absolute_url())
    elif 'POST'==req.method:
        valForm = ValForm(req.POST)
        if valForm.is_valid():
            validator = Validator.objects.get(user__username=valForm.cleaned_data['username'],
                hash=valForm.hash)
            validator.delete()
            newUser = authenticate(username=valForm.cleaned_data['username'],
                password=valForm.cleaned_data['code'])
            newUser.is_active = True
            login(req, newUser)
            newUser.set_unusable_password()
            newUser.save()
            return HttpResponseRedirect('/accounts/registration/password/')
    else:
        try:
            valForm = ValForm(initial={
                'username': req.GET['user'],
                'code': req.GET['code'],
            })
        except KeyError:
            valForm = ValForm()
    
    return render_to_response('registration/checkemail.html', {'valForm': valForm},
        context_instance=RequestContext(req))

@login_required
def make_password(req):
    if 'POST'==req.method:
        passForm = PassForm(req.POST)
        if passForm.is_valid():
            req.user.set_password(passForm.cleaned_data['password'])
            req.user.save()
            req.user.message_set.create(message=_('new password successfully set'))
            return HttpResponseRedirect(req.user.get_absolute_url())
    else:
        passForm = PassForm()
    
    return render_to_response('registration/password.html',
        {'passForm': passForm}, context_instance=RequestContext(req))
