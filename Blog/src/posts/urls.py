from django.urls import path

from .views import (
    posts_list,
    posts_update,
    posts_create,
    posts_delete,
    posts_detail
)

urlpatterns = [
    path('', posts_list, name='list'),

    path('create', posts_create),
    path('<slug:slug>/', posts_detail, name='detail'),
    path('<slug:slug>/edit/', posts_update, name='update'),
    path('<int:id>/delete', posts_delete)
]
