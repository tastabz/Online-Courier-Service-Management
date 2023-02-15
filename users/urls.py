from django.contrib.auth import views as auth_views
from django.urls import path

from users import views as user_views

app_name = 'users'

"""Contains all the urls to access users views."""

urlpatterns = [
    path('', user_views.home, name='home'),
    path('signup/', user_views.CustomerCreationView.as_view(), name='customer_signup'),
    path('user/<int:pk>/', user_views.UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/update', user_views.UserUpdateView.as_view(), name='user_update'),
    path('customer/<int:pk>/', user_views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/<int:pk>/update', user_views.CustomerUpdateView.as_view(), name='customer_update'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
