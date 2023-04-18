from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView
from .models import Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404

class TaskList(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm()
        return context
    
class TaskCreate(View):
    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
        return redirect('task_list')