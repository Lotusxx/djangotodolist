from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView
from .models import Task
from .forms import TaskForm
from django.forms import DateInput

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

#UpdateViewを使う場合
class TaskUpdate(UpdateView):
    model = Task
    fields = ['title', 'due_date']
    template_name = 'task_edit.html'
    success_url = reverse_lazy('task_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['due_date'].widget = DateInput(attrs={'type': 'date'})  # due_dateフィールドのウィジェットを上書き
        return form