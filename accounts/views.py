from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm
from etc.choices import USER_TYPE_CHOICES
from .models import OTP, CustomUser
from etc.helper_functions import OTP_random_digits
from etc.gmail_messages import send_registration_otp
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout


def create_user_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.type = USER_TYPE_CHOICES[1][0]
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            random_otp = OTP_random_digits()
            OTP.objects.create(user=user, otp_code=random_otp)
            send_registration_otp(request, random_otp, user.username, user.email)
            request.session['pending_user_id'] = user.id
            return redirect('accounts-customized-url:verify-mail-url')

    else:
        form = CreateUserForm()

    context = {
        "page_title": "Sign Up",
        "form" : form,
    }
    return render(request, 'registration/sign-up.html', context)



def verify_mail_view(request):
    user_id = request.session.get("pending_user_id")
    if not user_id:
        return redirect('accounts-customized-url:create-user-url')
    
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        try:
            otp_obj = OTP.objects.filter(user=user).latest("created_at")
        except OTP.DoesNotExist:
            messages.error(request, "No OTP found. Please request a new one.")
            return redirect("resend_otp")  # TODO: make resend page

        if otp_obj.is_used:
            messages.error(request, "This OTP was already used.")
        elif timezone.now() > otp_obj.expires_at:
            messages.error(request, "Your OTP has expired. Please request a new one.")
        elif not check_password(str(entered_otp), otp_obj.otp_code):
            otp_obj.attempts_count += 1
            otp_obj.save()
            messages.error(request, "Invalid OTP. Please try again.")
        else:
            otp_obj.is_used = True
            otp_obj.save()
            user.is_active = True
            user.save()
            messages.success(request, "Email verified successfully! You can now log in.")
            request.session.flush()   # deletes current session data + session cookie
            logout(request)
            return redirect("login")
    
    context = {
        "page_title": "Email verification"
    }

    return render(request, "registration/verify_otp.html", {"user": user}, context)


def log_out_view(request):
    request.session.flush()   # deletes current session data + session cookie
    logout(request)
    context = {
        "page_title": "Log-out"
    }
    return render(request, "registration/logout.html", context)
