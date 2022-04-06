from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from .filters import *
from .forms import *
from .decorators import unauthenticated_user, allowedUsers, adminonly


# Create your views here.

def registrerPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                group = Group.objects.get(name='customer')
                user.groups.add(group)

                Customer.objects.create(
                    user = user,
                )
                messages.success(request, 'Account for "{}" was created successfully'.format(username))
                return redirect('accounts:login')
        context = {'registerform': form}
        return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.info(request, "Usename OR Password is incorrect !!!")


    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
@adminonly
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    total_customers = customers.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    outdelivery = orders.filter(status='Out for Delivery').count()
    context = {
        'orders': orders,
        'customers': customers,
        'pending': pending,
        'delivered': delivered,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'outdelivery': outdelivery,
    }

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    outdelivery = orders.filter(status='Out for Delivery').count()
    context = {
        'orders':orders,
        'total_orders':total_orders,
        'delivered': delivered,
        'pending': pending,
        'outdelivery': outdelivery,
    }
    return render(request, "accounts/user.html", context)


@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method=='POST':
        form =CustomerForm(request.POST,request.FILES, instance=customer, )
        if form.is_valid():
            form.save()
            return redirect('accounts:account')
    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def products(request):
    prod = Product.objects.all()
    context = {
        'products': prod
    }
    return render(request, 'accounts/products/products.html', context)


@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def add_product(request):
    prodform = ProductForm()
    if request.method == 'POST':
        prodform = ProductForm(request.POST)
        if prodform.is_valid():
            prodform.save()
            return redirect('accounts:products', )
    context = {
        'product_form': prodform
    }
    return render(request, 'accounts/products/add_product.html', context)


@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def update_product(request, pk):
    prod = Product.objects.get(id=pk)
    prodform = ProductForm(instance=prod)
    if request.method == 'POST':
        prodform = ProductForm(request.POST, instance=prod)
        if prodform.is_valid():
            prodform.save()
            return redirect('accounts:products')

    context = {
        'product_form': prodform
    }
    return render(request, 'accounts/products/add_product.html', context)


@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def delete_product(request, pk):
    prod = Product.objects.get(id=pk)
    if request.method == 'POST':
        prod.delete()
        return redirect('accounts:products')
    context = {
        'prod': prod
    }
    return render(request, 'accounts/products/delete_product.html', context)


@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def customer(request, pk):
    custom = Customer.objects.get(id=pk)
    orders = custom.order_set.all()
    total_orders = orders.count()
    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs

    context = {
        'custom': custom,
        'orders': orders,
        'total_orders': total_orders,
        'filter_form': myfilter
    }

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    custom = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=custom)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=custom)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        'form': formset,
        'customer': custom
    }
    return render(request, 'accounts/orders/order_form.html', context)


@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'accounts/orders/order_form.html', context)


@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {
        'item': order
    }
    return render(request, 'accounts/orders/delete_order.html', context)
