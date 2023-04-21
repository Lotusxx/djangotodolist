from django.urls import path
from .views import TaskList, TaskCreate,TaskUpdate
#,TaskDelete,complete_task

urlpatterns = [
    path('', TaskList.as_view(), name='task_list'),
    path('create/', TaskCreate.as_view(), name='task_create'),
    path('<int:pk>/edit/', TaskUpdate.as_view(), name='task_edit'),
]