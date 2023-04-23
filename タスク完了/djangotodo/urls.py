from django.urls import path
from .views import TaskList, TaskCreate,TaskUpdate,TaskDelete,complete_task

urlpatterns = [
    path('', TaskList.as_view(), name='task_list'),
    path('create/', TaskCreate.as_view(), name='task_create'),
    path('<int:pk>/edit/', TaskUpdate.as_view(), name='task_edit'),
    path('<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'),
    path('<int:pk>/complete/', complete_task, name='task_complete'),
]