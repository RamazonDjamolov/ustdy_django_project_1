from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from .form import Forgot_password_form, RestorePasswordForm
from .service import send_email_alternative2


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        theme_color = request.POST['theme_color']
        if not username.strip() or not email.strip() or not password1.strip() or not password2.strip() or not theme_color.strip():
            messages.error(request, ('One of the fiels are empty! You should fill all field to Sign Up!'))
            return redirect('users:register')
        if password1 != password2:
            messages.error(request, ('Password is not equal to confirm password!'))
            return redirect('users:register')
        if len(password1) > 10 or len(password2) > 10:
            messages.error(request, ('Password can\'t be more than 10 letters!'))
            return redirect('users:register')
        if len(username) > 50:
            messages.error(request, ('Username can\'t be more than 50 elements!'))
            return redirect('users:register')
        if len(email) > 255:
            messages.error(request, ('Email can\'t be more than 255 elements!'))
            return redirect('users:register')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, ('This email already exists!'))
            return redirect('users:register')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, ('This username already exists!'))
            return redirect('users:register')
        else:
            user = CustomUser.objects.create_user(username=username, email=email, password=password1,
                                                  theme_color=theme_color)
            login(request, user)
            return redirect('posts:list')
    else:
        return render(request, 'users/register.html')


def login_view(request):
    user = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts:list')
        else:
            messages.error(request, ('There was an error please try again!'))
            return redirect('users:login')
    else:
        return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('users:login')


@login_required
def my_account(request):
    data = {
        'user': request.user
    }
    return render(request, 'users/my-account.html', context=data)


@login_required
def accounts_edit(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST['username']
        email = request.POST['email']
        theme_color = request.POST['theme_color']
        user.username = username
        user.email = email
        user.theme_color = theme_color
        user.save()
        return redirect('users:my-account')
    data = {
        'user': request.user
    }
    return render(request, 'users/accounts-edit.html', context=data)


@login_required
def home(request):
    return HttpResponse('salom')


def forgot_password(request):
    if request.method == 'POST':
        form = Forgot_password_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.filter(email=email).first()
            send_email_alternative2(email, user1=user)
            return HttpResponse("borib qara emailga kod bordi  ")
        return render(request, 'users/forgot_password.html', context={'form': form})

    form = Forgot_password_form
    return render(request, 'users/forgot_password.html', context={'form': form})



def restore_password(request):
    if request.method == 'POST':
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            form.update()
            return redirect('users:login')
        return render(request, 'users/restore.html', context={'form': form})
    form = RestorePasswordForm()
    return render(request, 'users/restore.html', context={'form': form})


