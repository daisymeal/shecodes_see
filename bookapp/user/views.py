from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm

from user.models import UserProfile

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth.models import User

def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user =request.user
            userprofile=UserProfile.objects.get(user_id=current_user.id)
            # request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,"Login Error !! username or Password is incorrect")
            return HttpResponseRedirect('/login')
   
    return render(request, 'user/login.html')    


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save()

            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template() 
            # and calls its render() method immediately.
            # message = render_to_string('user/activation_request.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     # method will generate a hash value with user related data
            #     'token': account_activation_token.make_token(user),
            # })
            # user.email_user(subject, message,'tramszone@gmail.com')
            # return redirect('activation_sent')   
            return redirect('home')   
            # messages.success(request, 'Your account has been created!')
            # return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/register')


    form = SignUpForm()
    #category = Category.objects.all()
    context = {
               'form': form,
               }
    return render(request, 'user/register.html', context)


def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')    


def activation_sent(request):
    return render(request, 'user/activation_sent.html')    


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.userprofile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('activated')
    else:
        return render(request, 'user/activation_invalid.html')    

def activated(request):
    return render(request, 'user/account_is_activated.html')   


def forgot_password(request):
    return render(request, 'user/forgot-password.html')       


@login_required(login_url='/login') # Check login
def userprofile(request):
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
               'profile':profile}
    return render(request,'user/user_profile.html',context)    

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {
        'form': form
    })    