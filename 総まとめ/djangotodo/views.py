from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView,DeleteView
from .models import Task
from .forms import TaskForm
from django.http import HttpResponse, JsonResponse
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
    
# class TaskUpdate(UpdateView):
#     model = Task
#     fields = ['title', 'due_date']
#     template_name = 'task_edit.html'
#     success_url = reverse_lazy('task_list')

#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         form.fields['due_date'].widget = DateInput(attrs={'type': 'date'})  # due_dateフィールドのウィジェットを上書き
#         return form

class TaskUpdate(View):
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            data = {
                'title': task.title,
                'due_date': str(task.due_date) if task.due_date else "",
            }
            return JsonResponse(data)
        else:
            errors = form.errors.as_json()
            return HttpResponse(errors, status=400, content_type='application/json')
    
class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')

def complete_task(request, pk):
    task = Task.objects.get(pk=pk)

    if task.is_completed:
        task.is_completed = False
    else:
        task.is_completed = True

    task.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'is_completed': task.is_completed
        }
    return JsonResponse(data)