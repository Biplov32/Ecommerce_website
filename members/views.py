from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from members.forms import SignupForm
from django.contrib import messages
# Create your views here.
def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')  
    else:
        form = SignupForm()
    return render(request, 'Register.html', {'form': form})

def login_user(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
           login(request, user)
           return redirect('home')
        else:
            return redirect('login_user') 
    else:
        return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('login_user')  #