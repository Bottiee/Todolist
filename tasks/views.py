from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.http import HttpResponseForbidden
from .models import Task
from .forms import TaskForm
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


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
            messages.success(request, 'New task added successfully!')
            return redirect('task-list')

    context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" updated successfully!')
            return redirect('task-list')
    else:
        form = TaskForm(instance=task)

    context = {'form': form, 'task': task}
    return render(request, 'tasks/task_update.html', context)


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)

    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f'Task "{task_title}" deleted successfully!')
        return redirect('task-list')

    context = {'task': task}
    return render(request, 'tasks/task_delete.html', context)

@login_required
def leaderboard(request):
    """
    Displays a leaderboard of users, ranked by completed tasks.
    """
    users_with_tasks = User.objects.annotate(
        total_tasks=Count('task'),
        completed_tasks=Count('task', filter=Q(task__completed=True))
    ).order_by('-completed_tasks', '-total_tasks') # Order by most completed, then most total

    context = {
        'users_list': users_with_tasks
    }
    return render(request, 'tasks/leaderboard.html', context)

@login_required
def superuser_dashboard(request):
    # 1. Check if the user is a superuser
    if not request.user.is_superuser:
        # If not, return a 'Forbidden' response
        return HttpResponseForbidden("You do not have permission to view this page.")

    # 2. Get all users and their tasks
    # We use prefetch_related to efficiently get all tasks for all users in one go
    all_users = User.objects.prefetch_related('task_set').all()

    # 3. Render the template with the data
    return render(request, 'tasks/superuser_dashboard.html', {'users': all_users})

@login_required
def user_profile(request):
    """
    Renders the user's profile page.
    """
    return render(request, 'tasks/profile.html')


@require_POST
@login_required
def update_task_order(request):
    try:
        # Get the ordered list of task IDs from the request body
        ordered_ids = json.loads(request.body).get('ordered_ids')

        if ordered_ids is None:
            return JsonResponse({'status': 'error', 'message': 'Missing ordered_ids'}, status=400)

        # Get all tasks for the current user that are in the list
        tasks = Task.objects.filter(user=request.user, id__in=ordered_ids)

        # Create a dictionary for quick lookup
        task_map = {task.id: task for task in tasks}

        # Update priority for each task based on the new order
        for index, task_id in enumerate(ordered_ids):
            if task_id in task_map:
                task = task_map[task_id]
                task.priority = index  # Set priority to the new index
                task.save()

        return JsonResponse({'status': 'success', 'message': 'Task order updated successfully.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)