from django.shortcuts import render, redirect
from .forms import *
from Main.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.
# registration
def register(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    
    # if they are not logged in
    else:
        if request.method == "POST":
            form = RegistrationForm(request.POST or None)
            # check if the form is valid
            if form.is_valid():
                user = form.save()

                # get the raw password
                raw_password = form.cleaned_data.get('password1')

                # authenticate the user
                user = authenticate(username=user.username, password=raw_password)

                # login the user
                login(request, user)
                messages.success(request,f'Your Account has been Created Successfully!')
                return redirect("main:home")
        else:
            form = RegistrationForm()
        return render(request, "accounts/register.html", {"form": form})


# login
def login_user(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            print(username, password)
            # check the credentials
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("main:home")
                else:
                    return render(request, 'accounts/login.html', {"error": "Your account has been disabled."})
            else:
                return render(request, 'accounts/login.html', {"error": "Invalid Username or Password. Try Again."})
        return render(request, 'accounts/login.html')

# logout user
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        print("Logged out succesfully")
        return redirect("accounts:login")
    else:
        return redirect("accounts:login")



@login_required
def profile(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else :
        item = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']
        
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect("main:profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'cartItems':cartItems
    }

    return render(request, 'main/profile.html', context)


