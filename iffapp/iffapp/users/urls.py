from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.UserRedirectView.as_view(), name='detail'),
    path('~redirect', views.UserRedirectView.as_view(), name='redirect'),
    path('~update/', views.UserUpdateView.as_view(), name='update'),
    path('<username>', views.UserDetailView.as_view(), name='detail'),
    path('create', views.UserCreateView.as_view(), name='create'),
]
