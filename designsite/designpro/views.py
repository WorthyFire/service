from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import RegistrationForm, DesignRequestForm, DesignCategoryForm, DesignRequestFilterForm, \
    ChangeRequestStatusForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from .models import CustomUser, DesignCategory
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
    custom_user = CustomUser.objects.get(user=request.user)
    my_requests = DesignRequest.objects.filter(user=custom_user)

    filter_form = DesignRequestFilterForm(request.GET)

    if filter_form.is_valid():
        status = filter_form.cleaned_data['status']
        if status:
            my_requests = my_requests.filter(status=status)

    context = {
        'my_requests': my_requests,
        'filter_form': filter_form,
    }

    return render(request, 'autorized/my_design_requests.html', context)

def request_detail(request, request_id):
    design_request = get_object_or_404(DesignRequest, pk=request_id)

    context = {
        'request': design_request,
        'user': request.user,  # Добавляем пользователя в контекст
    }

    return render(request, 'autorized/request_detail.html', context)

@login_required
def delete_request(request, pk):
    design_request = get_object_or_404(DesignRequest, pk=pk)

    if design_request.user.user != request.user:
        raise Http404("Вы не можете удалить эту заявку.")

    if design_request.status in ["Принято в работу", "Выполнено"]:
        raise Http404("Вы не можете удалить заявку со статусом \"Принято в работу\" или \"Выполнено\".")

    design_request.delete()

    return redirect('my_design_requests')

@user_passes_test(lambda u: u.is_staff)
def all_user_requests(request):
    user_requests = DesignRequest.objects.all()
    return render(request, 'staff/all_user_requests.html', {'user_requests': user_requests})
#Место для изменения статуса заявки
def change_request_status(request, request_id):
    if request.user.is_staff:
        design_request = DesignRequest.objects.get(pk=request_id)
        if design_request.status == 'Новая':
            if request.method == 'POST':
                form = ChangeRequestStatusForm(request.POST)
                if form.is_valid():
                    new_status = form.cleaned_data['status']
                    design_request.status = new_status
                    design_request.save()
                    return redirect('request_detail', request_id)
            else:
                form = ChangeRequestStatusForm()
            return render(request, 'staff/change_request_status.html', {'request': design_request, 'form': form})
        else:
            error_message = "У этой заявки нельзя изменить статус, так как её статус 'Принято в работу' или 'Выполнено'."
            messages.error(request, error_message)
            return redirect('request_detail', request_id)
    else:
        messages.error(request, 'У вас нет прав для изменения статуса заявки.')
        return redirect('request_detail', request_id)
###
def manage_categories(request):
    categories = DesignCategory.objects.all()
    form = DesignCategoryForm()

    if request.method == 'POST':
        form = DesignCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')

    return render(request, 'staff/manage_categories.html', {'categories': categories, 'form': form})

def delete_category(request, category_id):
    category = DesignCategory.objects.get(pk=category_id)
    category.delete()
    return redirect('manage_categories')














