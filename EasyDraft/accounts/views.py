from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from forms import CreateUserForm
from models import UserProfile

def register(request):
    next = request.REQUEST.get('next', '')
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            UserProfile.objects.create(user=new_user)
            new_user = authenticate(username=new_user.username, password=request.POST['password1'])
            print new_user
            if new_user is not None and new_user.is_active:
                login(request, new_user)
            return HttpResponseRedirect(request.POST['next'])
    else:
        form = CreateUserForm()
    return render_to_response("registration/register.html", locals(), context_instance=RequestContext(request))

@login_required
def delete(request):
    user = request.user
    deleted = True
    try:
        for test in user.get_profile().spamtest_set.all():
            test.delete()
        user.get_profile().delete()
        user.delete()
        del user
    except Exception, e:
        print e
        deleted = False
    logout(request)
    return render_to_response("registration/delete.html", locals(), context_instance=RequestContext(request))

@login_required
def change_email(request):
    success = False
    if request.method == 'POST':
        if request.POST['email_address']:
            user = request.user
            user.email = request.POST['email_address']
            user.save()
            success = True
    return render_to_response("registration/change_email.html", locals(), context_instance=RequestContext(request))

@login_required
def change_pass(request):
    pass

def reset_pass(request):
    pass
