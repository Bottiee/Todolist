from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.shortcuts import redirect
from .forms import TaskForm
from django.contrib.auth.views import LogoutView

def home(request):
    return render(request, 'tasks/home.html')

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

def profile_redirect(request):
    return redirect('task-list')

class LogoutGetAllowedView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@login_required
def main_profile(request):
    user = request.user
    tasks = Task.objects.filter(user=user).order_by('-created_at')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = user
            new_task.save()
            return redirect('main-profile')
    else:
        form = TaskForm()

    context = {
        'tasks': tasks,
        'form': form,
    }
    return render(request, 'tasks/mainprofile.html', context)