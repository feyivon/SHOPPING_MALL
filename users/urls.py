from django.urls import path
from users.views import register, logoutConfirm
from django.contrib.auth.views import (LoginView, LogoutView, 
                                       PasswordResetView, PasswordResetDoneView, 
                                       PasswordResetConfirmView, PasswordResetCompleteView)

urlpatterns = [
    path('user/register/', register, name='register_account'),
    path('user/account/login/', LoginView.as_view(template_name='users/loginPage.html'), name='loginPage'),
    path('user/account/logout/', LogoutView.as_view(), name='user_logout'),
    path('user/confirm/logout/', logoutConfirm, name='logout_confirm'),

    # getting user email for password reset
    path('user/password/reset/', PasswordResetView.as_view(template_name='users/password_rest_view.html'), name='password_reset'),

    # showing that an email have been sent for password reset
    path('user/password/reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),

    # the form to reset password
    path('user/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),

    # showing that the reset password is fully done
    path('user/password/reset/complete/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]