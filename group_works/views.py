from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Project, Task
from .forms import ProjectForm, TaskForm, ProjectDeleteForm, TaskDeleteForm


def home(request):
    """The home page for Group Work."""
    return render(request, 'group_works/home.html')


class ProjectListView(ListView):
    model = Project
    template_name = 'group_works/project-list.html'
    context_object_name = 'projects'
    ordering = ['due_date']
    paginate_by = 5

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user).order_by('due_date')


@login_required
def task_list(request, project_pk):
    """Show all tasks for requested project."""
    project = get_object_or_404(Project, id=project_pk)
    # Make sure topic belongs to current user
    __check_project_owner__(project.owner, request.user)

    tasks = project.task_set.order_by('due_date')
    context = {'project': project, 'tasks': tasks}
    return render(request, 'group_works/task_list.html', context)

# class TaskListView(ListView):
#     """Equivalent to task_list, but I couldn't figure out
#     how to display project name from queryset of tasks
#     on the template."""
#     model = Task
#     template_name = 'group_works/task-list.html'
#     context_object_name = 'tasks'
#     ordering = ['due_date']
#     paginate_by = 5
#
#     def get_queryset(self):
#         proj = get_object_or_404(Project, pk=self.kwargs['project_pk'])
#         return Task.objects.filter(project=proj).order_by('due_date')
#
#     def get_context_data(self, **kwargs):
#         context = super(TaskListView, self).get_context_data(**kwargs)
#         context['project'] = Project.objects.filter(
#             pk=self.kwargs['project_pk']).get()
#         return context


class TaskDetailView(DetailView):
    model = Task
    pk_url_kwarg = 'task_pk'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['title', 'due_date', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'due_date', 'description']
    pk_url_kwarg = 'project_pk'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.owner:
            return True
        return False


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    success_url = '/'

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.owner:
            return True
        return False


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'due_date', 'description']

    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk=self.kwargs['project_pk'])
        form.instance.project.owner = self.request.user
        return super().form_valid(form)


class TaskEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'due_date', 'description']

    def form_valid(self, form):
        form.instance.project.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.project.owner:
            return True
        return False


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    success_url = '/'

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.project.owner:
            return True
        return False


def about(request):
    return render(request, 'group_works/about.html', {'title': 'About'})


def __check_project_owner__(owner, user):
    """Check if the user has access to a page.
    Raise a 404 error if not."""
    if owner != user:
        raise Http404

# @login_required
# def projects(request):
#     """Show all projects."""
#     projects = Project.objects.filter(owner=request.user).order_by('due_date')
#     context = {'projects': projects}
#     return render(request, 'group_works/projects.html', context)

# @login_required
# def project(request, project_id):
#     """Show all tasks for requested project."""
#     project = get_object_or_404(Project, id=project_id)
#     # Make sure topic belongs to current user
#     __check_project_owner__(project.owner, request.user)
#
#     tasks = project.task_set.order_by('due_date')
#     context = {'project': project, 'tasks': tasks}
#     return render(request, 'group_works/project.html', context)

# @login_required
# def task(request, task_id):
#     """Show info for a task."""
#     task = get_object_or_404(Task, id=task_id)
#     project = task.project
#     __check_project_owner__(project.owner, request.user)
#
#     context = {'task': task, 'project': project}
#     return render(request, 'group_works/task.html', context)

# @login_required
# def new_project(request):
#     """Add a new project."""
#     if request.method != 'POST':
#         form = ProjectForm()
#     else:
#         form = ProjectForm(data=request.POST)
#         if form.is_valid():
#             new_project = form.save(commit=False)
#             new_project.owner = request.user
#             new_project.save()
#             return redirect('group_works:projects')  # in the future i want this to redirect to the new project page
#
#     context = {'form': form}
#     return render(request, 'group_works/new_project.html', context)

# @login_required
# def edit_project(request, project_id):
#     """Edit an existing project."""
#     project = Project.objects.get(id=project_id)
#     __check_project_owner__(project.owner, request.user)
#
#     if request.method != 'POST':
#         form = ProjectForm(instance=project)
#     else:
#         form = ProjectForm(instance=project, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('group_works:project', project_id=project.id)
#
#     context = {'project': project, 'form': form}
#     return render(request, 'group_works/edit_project.html', context)

# @login_required
# def new_task(request, project_id):
#     """Add a new task."""
#     project = Project.objects.get(id=project_id)
#     __check_project_owner__(project.owner, request.user)
#
#     if request.method != 'POST':
#         form = TaskForm()
#     else:
#         form = TaskForm(data=request.POST)
#         if form.is_valid():
#             new_task = form.save(commit=False)
#             new_task.project = project
#             new_task.save()
#             return redirect('group_works:project', project_id=project_id)
#
#     context = {'project': project, 'form': form}
#     return render(request, 'group_works/new_task.html', context)
#
#
# @login_required
# def edit_task(request, task_id):
#     """Edit an existing task."""
#     task = Task.objects.get(id=task_id)
#     project = task.project
#     __check_project_owner__(project.owner, request.user)
#
#     if request.method != 'POST':
#         form = TaskForm(instance=task)
#     else:
#         form = TaskForm(instance=task, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('group_works:project', project_id=project.id)
#
#     context = {'task': task, 'project': project, 'form': form}
#     return render(request, 'group_works/edit_task.html', context)
#
#
# @login_required
# def delete_project(request, project_id):
#     project = Project.objects.get(id=project_id)
#     __check_project_owner__(project.owner, request.user)
#
#     if request.method != 'POST':
#         form = ProjectDeleteForm(instance=project)
#     else:
#         form = ProjectDeleteForm(instance=project, data=request.POST)
#         if form.is_valid():
#             project.delete()
#             return redirect('group_works:projects')
#
#     context = {'project': project, 'form': form}
#     return render(request, 'group_works/delete_project.html', context)
#
#
# @login_required
# def delete_task(request, task_id):
#     task = Task.objects.get(id=task_id)
#     project = task.project
#     __check_project_owner__(project.owner, request.user)
#
#     if request.method != 'POST':
#         form = TaskDeleteForm(instance=task)
#     else:
#         form = TaskDeleteForm(instance=task, data=request.POST)
#         if form.is_valid():
#             task.delete()
#             print('deleted')
#             return redirect('group_works:project', project_id=project.id)
#
#     context = {'task': task, 'project': project, 'form': form}
#     return render(request, 'group_works/delete_task.html', context)
#
#

