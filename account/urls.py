from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # login url patterns
    # previous login
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # dashboard url pattern
    path('', views.dashboard, name='dashboard'),

    # password change url patterns
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    # register urls
    path('register/', views.register, name='register'),

    # edit profile
    path('edit/', views.edit, name='edit'),

    # add follow view (is placed BEFORE user_detail pattern due to similarity)
    path('users/follow/', views.user_follow, name='user_follow'),

    # add user views
    path('users/', views.user_list, name='user_list'),
    path('users/<username>/', views.user_detail, name='user_detail'),
]
