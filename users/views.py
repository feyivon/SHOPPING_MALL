from django.shortcuts import render, redirect
from users.forms import UserResgisterForm

# Create your views here.
def register(request):
    form = UserResgisterForm()
    if request.method == 'POST':
        user = UserResgisterForm(request.POST)
        if user.is_valid():
            user.save()
            return redirect('loginPage')
    else:
        form = UserResgisterForm()
    context = {
        'form' : form
    }
    return render(request, 'users/register.html', context)

def logoutConfirm(request):
    return render(request, 'users/logout_confirm.html')