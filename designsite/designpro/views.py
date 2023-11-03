from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import RegistrationForm, DesignRequestForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import CustomUser
from .models import DesignRequest


def home(request):
    completed_requests = DesignRequest.objects.filter(status='Выполнено').order_by('-created_at')[:4]
    in_progress_count = DesignRequest.objects.filter(status='Принято в работу').count()

    context = {
        'completed_requests': completed_requests,
        'in_progress_count': in_progress_count,
    }

    return render(request, 'home.html', context)


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

            # Создаем объект CustomUser и связываем его с пользователем
            custom_user, created = CustomUser.objects.get_or_create(user=user, defaults={'full_name': full_name})

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

    my_requests = DesignRequest.objects.filter(user=request.user.customuser)

    context = {
        'my_requests': my_requests,
    }

    return render(request, 'autorized/my_design_requests.html', context)

def request_detail(request, request_id):
    design_request = get_object_or_404(DesignRequest, pk=request_id)

    context = {
        'request': design_request,
    }

    return render(request, 'autorized/request_detail.html', context)

@login_required
def delete_design_request(request, request_id):
    # Получаем заявку
    design_request = get_object_or_404(DesignRequest, pk=request_id)

    # Проверяем, что текущий пользователь - автор заявки
    if design_request.user.user != request.user:
        raise Http404("Вы не можете удалить эту заявку.")

    # Удаляем заявку
    design_request.delete()

    return redirect('my_design_requests')

def delete_request(request, pk):
    design_request = DesignRequest.objects.get(pk=pk)
    design_request.delete()
    return redirect('my_design_requests')
















