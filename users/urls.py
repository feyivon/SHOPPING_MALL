from django.urls import path
from users.views import register, logoutConfirm
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('user/register/', register, name='register_account'),
    path('user/account/login/', LoginView.as_view(template_name='users/loginPage.html'), name='loginPage'),
    path('user/account/logout/', LogoutView.as_view(), name='user_logout'),
    path('user/confirm/logout', logoutConfirm, name='logout_confirm')
]