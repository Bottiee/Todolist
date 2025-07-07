from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .models import Task
from .forms import TaskForm

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

@login_required
def task_list(request):
    """
    Handles both displaying a user's tasks and creating a new task.
    This is our main view.
    """
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('task-list')

    context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_update(request, pk):
    """
    Handles updating an existing task.
    """
    task = get_object_or_404(Task, id=pk, user=request.user) # Ensures user owns this task
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-list')

    context = {'form': form, 'task': task}
    return render(request, 'tasks/task_update.html', context)


@login_required
def task_delete(request, pk):
    """
    Handles deleting an existing task.
    """
    task = get_object_or_404(Task, id=pk, user=request.user) # Ensures user owns this task

    if request.method == 'POST':
        task.delete()
        return redirect('task-list')

    context = {'task': task}
    return render(request, 'tasks/task_delete.html', context)