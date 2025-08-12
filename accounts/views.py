from django.shortcuts import render, redirect
from .forms import CreateUserForm
from etc.choices import USER_TYPE_CHOICES


def create_user_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.type = USER_TYPE_CHOICES[1][0]
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            return redirect() # TODO: redirect to email OTP page

    else:
        form = CreateUserForm()

    context = {
        "page_title": "Sign Up",
        "form" : form,
    }
    return render(request, 'registration/sign-up.html', context)