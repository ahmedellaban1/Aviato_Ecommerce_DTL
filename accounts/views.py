from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CreateUserForm, UpdateProfileForm, CreateUpdateAddressForm
from .models import OTP, CustomUser, Profile, Address
from etc.choices import USER_TYPE_CHOICES
from etc.helper_functions import OTP_random_digits
from etc.gmail_messages import send_registration_otp
from etc.decorators import client_required



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
            try:
                user = CustomUser.objects.only('id').get(id=user_id)
                random_otp = OTP_random_digits()
                OTP.objects.create(user=user, otp_code=random_otp)
                send_registration_otp(request, random_otp, user.username, user.email)
                request.session['pending_user_id'] = user.id
                return redirect('accounts-customized-url:verify-mail-url')
            except CustomUser.DoesNotExist:
                return redirect('accounts-customized-url:create-user-url')

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
            
            # deletes current session data + session cookie
            request.session.flush()
            logout(request)
            return redirect("login")
    
    context = {
        "page_title": "Email verification",
        "user": user,
    }

    return render(request, "registration/verify_otp.html", context)


def log_out_view(request):

    # If the user is already logged out, send them home
    if not request.user.is_authenticated:
        return redirect('products-main-url:home-page-url')
    
    # deletes current session data + session cookie
    request.session.flush()
    logout(request)

    context = {
        "page_title": "Log-out"
    }
    return render(request, "registration/log_out.html", context)


@login_required
@client_required
def profile_details_view(request):
    profile = (
        Profile.objects
        .select_related("user")
        .only("id", "user__first_name", "user__last_name",
               "user__email", "image", "country", "phone", 
               "date_of_birth", "gender"
        )
        .defer("user__password")
        .get(user=request.user)
    )
    context = {
        "page_title": f"{profile.user.first_name} {profile.user.last_name}" or None,
        "profile": profile
    }
    return render(request, 'profile_details.html', context)


@login_required
@client_required
def update_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts-customized-url:profile-details-url')
    else:
        form = UpdateProfileForm(instance=profile)
    context = {
        "page_title": "Update my profile",
        "form": form
    }
    return render(request, 'update_profile.html', context)


@login_required
@client_required
def client_address_view(request):
    addresses = Address.objects.only('id', 'company', 'address', 'country', 'phone').filter(user=request.user)
    
    context = {
        "page_title": "Address",
        "addresses": addresses,
    }
    return render(request, 'address.html', context)


@login_required
@client_required
def add_address_view(request):
    if request.method == "POST":
        form = CreateUpdateAddressForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, "Address added successfully !")
            return redirect('accounts-customized-url:client-address-url')
    else:
        form = CreateUpdateAddressForm()

    context = {
        "page_title": "Address",
        "form": form,
    }
    return render(request, 'add_address.html', context)


@require_POST
@login_required
@client_required
def delete_address_view(request):
    method = request.POST.get('_method')
    if method == "DELETE":
        address_id = request.POST.get('address_id')
        address = get_object_or_404(Address, id=int(address_id), user=request.user)
        address.delete()
        messages.success(request, "Address deleted successfully!")

    return redirect('accounts-customized-url:client-address-url')


@login_required
@client_required
def updat_address_view(request, **kwargs):
    address = get_object_or_404(Address, id=kwargs['pk'], user=request.user)
    if request.method == "POST":
        form = CreateUpdateAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully!")
            return redirect('accounts-customized-url:client-address-url')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CreateUpdateAddressForm(instance=address)

    context = {
        "page_title": f"Update address {address.address[:10]}",
        "form": form
    }
    return render(request, 'edit_address.html', context)
