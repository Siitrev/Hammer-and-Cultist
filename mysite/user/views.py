from django.shortcuts import render, redirect, HttpResponse
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .token import account_activation_token, default_password_token
from django.core.mail import EmailMessage
# Create your views here.
def register_request(request):
    errors = {"user_error":False,"email_error":False,"pass_error":False}
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activation link has been sent to your email"
            message = render_to_string("user/acc_active_email.html",{
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject,message,to=[to_email])
            email.send()
            return render(request=request, template_name="user/token_send.html")
        username = request.POST["username"]
        email = request.POST["email"]
        if User.objects.filter(username=username).exists():
            errors["user_error"]=True
        if User.objects.filter(email=email).exists():
            errors["email_error"]=True
        if not errors["user_error"] and not errors["email_error"]:
            errors["pass_error"] = True
    form = NewUserForm()
    context = {"register_form":form}
    context.update(errors)
    return render(request=request, template_name="user/register.html", context=context)

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}." )
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password")
    form = AuthenticationForm()
    return render(request=request, template_name="user/login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    return redirect("home")

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return render(request=request, template_name="user/acc_verification_success.html", context={"username": user.get_username()})
    else:  
        return render(request=request, template_name="user/error.html")
    

def password_reset_request(request):
    errors = {"email_error":False}
    if request.method == "POST":
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            to_email = form.cleaned_data.get("email")
            if User.objects.filter(email=to_email).exists():
                user = User.objects.get(email=to_email)
                current_site = get_current_site(request)
            mail_subject = "Password reset link"
            message = render_to_string("user/acc_reset_pass.html",{
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_password_token.make_token(user),
            })
            email = EmailMessage(mail_subject,message,to=[to_email])
            email.send()
            return render(request=request, template_name="user/password_reset_send.html")
                
        errors["email_error"]=True
    form = PasswordResetForm()
    context = {"password_reset_form":form}
    context.update(errors)
    return render(request=request, template_name="user/password_reset.html", context=context)

def password_reset_change(request,uidb64,token):
    User = get_user_model() 
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if request.method == "POST":
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            return render(request=request, template_name="user/password_reset_success.html")
        else:
            return render(request=request, template_name="user/password_reset_change.html", context={"change_password_form":form, "form_errors": form.errors})
    else:  
        if user is not None and default_password_token.check_token(user, token):
            form = SetPasswordForm(user=user)
            return render(request=request, template_name="user/password_reset_change.html", context={"change_password_form":form})
        else:  
            return render(request=request, template_name="user/error.html")
    