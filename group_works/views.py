from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages

from .models import Project, Task
from .forms import ProjectForm, TaskForm, ProjectDeleteForm, TaskDeleteForm

# Create your views here.


def home(request):
    """The home page for Group Work."""
    return render(request, 'group_works/home.html')


@login_required
def projects(request):
    """Show all projects."""
    projects = Project.objects.filter(owner=request.user).order_by('due_date')
    context = {'projects': projects}
    return render(request, 'group_works/projects.html', context)


@login_required
def project(request, project_id):
    """Show all tasks for requested project."""
    project = get_object_or_404(Project, id=project_id)
    # Make sure topic belongs to current user
    __check_project_owner__(project.owner, request.user)

    tasks = project.task_set.order_by('due_date')
    context = {'project': project, 'tasks': tasks}
    return render(request, 'group_works/project.html', context)


@login_required
def task(request, task_id):
    """Show info for a task."""
    task = get_object_or_404(Task, id=task_id)
    project = task.project
    __check_project_owner__(project.owner, request.user)

    context = {'task': task, 'project': project}
    return render(request, 'group_works/task.html', context)


@login_required
def new_project(request):
    """Add a new project."""
    if request.method != 'POST':
        form = ProjectForm()
    else:
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = request.user
            new_project.save()
            return redirect('group_works:projects')  # in the future i want this to redirect to the new project page

    context = {'form': form}
    return render(request, 'group_works/new_project.html', context)


@login_required
def edit_project(request, project_id):
    """Edit an existing project."""
    project = Project.objects.get(id=project_id)
    __check_project_owner__(project.owner, request.user)

    if request.method != 'POST':
        form = ProjectForm(instance=project)
    else:
        form = ProjectForm(instance=project, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_works:project', project_id=project.id)

    context = {'project': project, 'form': form}
    return render(request, 'group_works/edit_project.html', context)


@login_required
def new_task(request, project_id):
    """Add a new task."""
    project = Project.objects.get(id=project_id)
    __check_project_owner__(project.owner, request.user)

    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(data=request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.project = project
            new_task.save()
            return redirect('group_works:project', project_id=project_id)

    context = {'project': project, 'form': form}
    return render(request, 'group_works/new_task.html', context)


@login_required
def edit_task(request, task_id):
    """Edit an existing task."""
    task = Task.objects.get(id=task_id)
    project = task.project
    __check_project_owner__(project.owner, request.user)

    if request.method != 'POST':
        form = TaskForm(instance=task)
    else:
        form = TaskForm(instance=task, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_works:project', project_id=project.id)

    context = {'task': task, 'project': project, 'form': form}
    return render(request, 'group_works/edit_task.html', context)


@login_required
def delete_project(request, project_id):
    project = Project.objects.get(id=project_id)
    __check_project_owner__(project.owner, request.user)

    if request.method != 'POST':
        form = ProjectDeleteForm(instance=project)
    else:
        form = ProjectDeleteForm(instance=project, data=request.POST)
        if form.is_valid():
            project.delete()
            return redirect('group_works:projects')

    context = {'project': project, 'form': form}
    return render(request, 'group_works/delete_project.html', context)


@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    project = task.project
    __check_project_owner__(project.owner, request.user)

    if request.method != 'POST':
        form = TaskDeleteForm(instance=task)
    else:
        form = TaskDeleteForm(instance=task, data=request.POST)
        if form.is_valid():
            task.delete()
            print('deleted')
            return redirect('group_works:project', project_id=project.id)

    context = {'task': task, 'project': project, 'form': form}
    return render(request, 'group_works/delete_task.html', context)


def __check_project_owner__(owner, user):
    """Check if the user has access to a page.
    Raise a 404 error if not."""
    if owner != user:
        raise Http404
