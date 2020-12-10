from django.urls import path

from . import views

urlpatterns = [
    path("new", views.create_task_render, name="new-task"),
    path("new-saved", views.create_task, name="new-task-saved"),
    path('details/<str:id>', views.get_single_task, name='task-details'),
    path('status/<str:id>', views.update_status, name='update-status'),
    path('delete/<str:id>', views.delete_task, name='delete-task'),
    path('delete-all', views.delete_all_task, name='delete-all-task'),
    path('change/<str:id>', views.update_task_render, name="update-task"),
    path('update/current/<str:id>', views.update_task, name='update-current-task')
]
