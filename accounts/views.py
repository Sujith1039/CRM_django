from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import Group
from .models import *
from .forms import OrderForm, CustomerForm, CreateUserForm, UserForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorcators import *

@unauthenticated_user
def register(request):
        
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                
                username = form.cleaned_data.get('username')
                messages.success(request,'Account has been created for ' + username)
                return redirect('login')
            else:
                print(form.errors)
        else:
            form = CreateUserForm()
        context = {'form': form}
        return render(request,'accounts/register.html', context)

@unauthenticated_user
def loginUser(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('user')
            else:
                messages.info(request,"username or password in not correct")
        return render(request, 'accounts/login.html')
    
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def dashboard(request):
    customers = Customer.objects.all()
    total_customers = customers.count()
    orders = Orders.objects.all()
    total_orders = orders.count()
    context = {'total_customers': total_customers , 'total_orders': total_orders}
    return render(request, 'accounts/dashboard.html', context)
 
@login_required(login_url='login')
def products(request):
    products = Products.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'customer'])
def user(request):
    orders = request.user.customer.orders_set.all()
    context={'orders': orders}
    return render(request,'accounts/user.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'customer'])
def account_settings(request):
    customer = request.user.customer
    form = UserForm(instance=customer)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES,  instance=customer)
        if form.is_valid():
            form.save()
    context={'form': form}
    return render(request, 'accounts/profile.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customers(request):
    customers = Customer.objects.all()   
    
    orders = Orders.objects.all()
    filter = OrderFilter(request.GET, queryset=orders)
    orders = filter.qs
    context = {'customers': customers, 'orders': orders, 'filter': filter}
    return render(request, 'accounts/customers.html', context)

@login_required(login_url='login')
def customers_unique(request, pk):
    customer = Customer.objects.get(id=pk)   
    orders = customer.orders_set.all()
    context = {'customers': customer, 'orders': orders}
    return render(request, 'accounts/customer_unique.html', context)

@login_required(login_url='login')
def createOrder(request):
    form = OrderForm()
    context = {'form': form}
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/customers')
    return render(request,'accounts/create_order.html', context) 

@login_required(login_url='login')
def createCustomer(request):
    form = CustomerForm()
    context = {'form': form}
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/customers')
    return render(request,'accounts/create_customer.html',context)

@login_required(login_url='login')
def updateCustomer(request,pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST , instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/customers')
    context ={'form':form} 
    return render(request,'accounts/create_customer.html', context)

@login_required(login_url='login')
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('/customers')
    context = {'customer': customer}
    return render(request, 'accounts/delete_customer.html', context)

@login_required(login_url='login')
def customerOrder(request,pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer':customer})
    context = {'form': form}
    if request.method == 'POST':
        form = OrderForm(request.POST, initial={'customer':customer})
        if form.is_valid():
            form.save()
            return redirect('/customers/{}'.format(pk))
    return render(request, 'accounts/create_order.html',context)
