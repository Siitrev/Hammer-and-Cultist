from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, HttpResponse
from .forms import NewUserForm, EditProfileForm
from blog.models import Post
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    SetPasswordForm,
    PasswordResetForm,
)
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .token import account_activation_token, default_password_token
from django.core.mail import EmailMessage
from django.http import HttpRequest, HttpResponse
from blog.handle_file import save_avatar

# Create your views here.
def register_request(request: HttpRequest):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data.get("email")
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activation link has been sent to your email"
            message = render_to_string(
                "user/acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request=request, template_name="user/token_send.html")
        else:
            return render(
                request=request,
                template_name="user/register.html",
                context={"register_form": form},
            )
    form = NewUserForm()
    return render(
        request=request,
        template_name="user/register.html",
        context={"register_form": form},
    )


def login_request(request: HttpRequest):
    next_path = ""
    if "next" in request.GET:
        next_path = request.GET["next"]
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                if next_path != "":
                    return redirect(next_path)
                return redirect("home")
            else:
                return render(
                    request=request,
                    template_name="user/login.html",
                    context={"login_form": form},
                )
        else:
            return render(
                request=request,
                template_name="user/login.html",
                context={"login_form": form},
            )
    form = AuthenticationForm()
    return render(
        request=request, template_name="user/login.html", context={"login_form": form}
    )


def logout_request(request: HttpRequest):
    logout(request)
    return redirect("home")


def activate(request: HttpRequest, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(
            request=request,
            template_name="user/acc_verification_success.html",
            context={"username": user.get_username()},
        )
    else:
        return render(request=request, template_name="user/error.html")


def password_reset_request(request: HttpRequest):
    if request.method == "POST":
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            to_email = form.cleaned_data.get("email")
            if User.objects.filter(email=to_email).exists():
                user = User.objects.get(email=to_email)
                current_site = get_current_site(request)
            else:
                form.add_error("email", error="Account with given email doesn't exist.")
                return render(
                    request=request,
                    template_name="user/password_reset.html",
                    context={"password_reset_form": form},
                )
            mail_subject = "Password reset link"
            message = render_to_string(
                "user/acc_reset_pass.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_password_token.make_token(user),
                },
            )
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(
                request=request, template_name="user/password_reset_send.html"
            )
        else:
            return render(
                request=request,
                template_name="user/password_reset.html",
                context={"password_reset_form": form},
            )
    form = PasswordResetForm()
    return render(
        request=request,
        template_name="user/password_reset.html",
        context={"password_reset_form": form},
    )


def password_reset_change(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if request.method == "POST":
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            return render(
                request=request, template_name="user/password_reset_success.html"
            )
        else:
            return render(
                request=request,
                template_name="user/password_reset_change.html",
                context={"change_password_form": form},
            )
    else:
        if user is not None and default_password_token.check_token(user, token):
            form = SetPasswordForm(user=user)
            return render(
                request=request,
                template_name="user/password_reset_change.html",
                context={"change_password_form": form},
            )
        else:
            return render(request=request, template_name="user/error.html")


def user_profile(request: HttpRequest, username):
    try:
        user_profile = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("Given user does not exist.")
    user_posts = Post.objects.filter(author=user_profile.pk, status=1).order_by(
        "-likes"
    )[:3]
    return render(
        request=request,
        template_name="user/user_profile.html",
        context={
            "username": username,
            "user_profile": user_profile,
            "user_posts": user_posts,
        },
    )


@login_required(login_url="/user/login/")
def edit_user_profile(request: HttpRequest, username):
    try:
        if request.user.username != username:
            return HttpResponse("You don't have permission to edit this profile.")
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("Given user does not exist.")
   
    if request.method == "GET":
        form = EditProfileForm(
            initial={
                "avatar": user.profile.avatar,
                "bio": user.profile.bio,
                "username": user.username,
            }
        )
        return render(
            request=request,
            template_name="user/edit_user_profile.html",
            context={
                "edit_profile_form": form,
            },
        )
        
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES)
        img = form.files.get("avatar", None)
        
        if not form.is_valid():
            return render(
            request=request,
            template_name="user/edit_user_profile.html",
            context={
                "edit_profile_form": form,
            },
        )
            
        new_username = form.cleaned_data.get("username")
        try:
            if img:
                img_path = save_avatar(img, new_username)
            elif username != new_username:
                img_path = save_avatar(user.profile.avatar.file, new_username, True)
        except ValidationError as e:
            form.add_error("avatar", e)
            return render(
                request=request,
                template_name="user/edit_user_profile.html",
                context={
                    "edit_profile_form": form,
            },
        )
            
        user.username = new_username
        user.profile.bio = form.cleaned_data.get("bio")
        if img or new_username != username:
            user.profile.avatar = img_path
        
        user.save()
        
        return redirect("user-profile", username)
                
                
        
        


class UserPosts(LoginRequiredMixin, generic.ListView):
    template_name = "user/user_posts.html"

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        try:
            user = User.objects.filter(
                username=self.kwargs["username"], pk=request.user.pk
            ).get()
        except User.DoesNotExist:
            return HttpResponse("Forbidden resource", status=403)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        user = self.kwargs["username"]
        queryset = Post.objects.filter(author_id__username=user).order_by("-created_on")
        return queryset
