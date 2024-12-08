from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import MyUserRegisterForm


def user_register_view(request):
    if request.method == 'POST':
        form = MyUserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно создан.')
            return redirect('main:main_index')

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')

    return redirect('main:main_index')


def user_login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Вы успешно вошли.')
            return redirect('main:main_index')

        messages.error(request, 'Неправильный логин или пароль. Попробуйте ещё раз!')
        return redirect('main:main_index')

    return redirect('main:main_index')


def user_logout_view(request):
    logout(request)
    return redirect('main:main_index')
