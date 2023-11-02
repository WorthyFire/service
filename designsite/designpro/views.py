from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import RegistrationForm, DesignRequestForm
from django.contrib.auth.models import User
from django.contrib.auth import login

from .models import CustomUser, DesignRequest


def home(request):
    return render(request, 'home.html')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.first_name = full_name
            user.save()

            custom_user = CustomUser(user=user, full_name=full_name)
            custom_user.save()

            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Неверный логин или пароль')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def dashboard(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'autorized/dashboard.html')
@login_required
def create_design_request(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user.customuser
            design_request.save()
            return redirect('dashboard')
    else:
        form = DesignRequestForm()

    return render(request, 'autorized/create_request.html', {'form': form})

def my_design_requests(request):
    # Получить CustomUser для текущего пользователя
    custom_user = CustomUser.get_custom_user(request.user)

    if custom_user:
        # Извлечь заявки для CustomUser
        my_requests = DesignRequest.objects.filter(user=custom_user)
    else:
        my_requests = []

    return render(request, 'autorized/my_design_requests.html', {'my_requests': my_requests})








