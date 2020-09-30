from django.shortcuts import render, redirect , get_object_or_404
from django.forms import inlineformset_factory

from .models import *

from .filters import OrderFilter

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .forms import OrderForm, CreateUserForm , CustomerForm

from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated,allowed_users,admin_only


@unauthenticated
def RegisterPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			

			messages.success(request, 'Account was created for ' + username)

			return redirect('accounts:login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)


@unauthenticated
def LoginPage(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request,user)
			return redirect('accounts:home')
		else:
			messages.info(request,'Username or password is incorrect')
	context = {}
	return render(request,'accounts/login.html',context)


def LogoutPage(request):
	logout(request)
	return redirect('accounts:login')


@allowed_users(allowed_roles=['customer'])
def UserPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}
	return render(request,'accounts/users.html',context)


@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=['customer'])
def AccountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES , instance=customer)
		if form.is_valid():
			form.save()


	context = {
		'form':form
		}
	return render(request, 'accounts/account_settings.html', context)


@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=['admin'])
def product(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html',{'products':products})


@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
	customer = Customer.objects.get(id=pk)	
	orders = customer.order_set.all()
	orders_count = orders.count()

	myFilter = OrderFilter(request.GET,queryset=orders)
	orders = myFilter.qs

	context = {
		'customer':customer,
		'orders':orders,
		'orders_count':orders_count,
		'myFilter' : myFilter,
		}


	return render(request, 'accounts/customer.html', context)


@login_required(login_url="accounts:login")
@admin_only
def dashboard(request):
	customers = Customer.objects.all()
	orders = Order.objects.all()
	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {
	'customers':customers,
	'orders':orders,
	'delivered':delivered,
	'pending':pending,
	'total_orders':total_orders,
	'total_customers':total_customers
	}

	return render(request, 'accounts/dashboard.html', context)



@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=['admin'])
def CreateOrder(request,pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'),extra=6)
	customer = Customer.objects.get(id=pk)
	# form = OrderForm(instance=customer,initial={'customer':customer})
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)



	if request.method=="POST":
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('../../')
	context = {'formset':formset}
	return render(request,'accounts/order_form.html',context)


@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=['admin'])
def UpdateOrder(request,pk):

	orders = Order.objects.get(id=pk)
	form = OrderForm(instance=orders)
		
	if request.method=="POST":
		form = OrderForm(request.POST, instance=orders)
		if form.is_valid():
			form.save()
			return redirect('../../')

	context = {'form':form}
	return render(request,'accounts/order_form.html',context)


@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=['admin'])
def DeleteOrder(request,pk):

	orders = get_object_or_404(Order,id=pk)

	if request.method=="POST":
		orders.delete()
		return redirect('../../')

	context = {'orders':orders}

	return render(request, 'accounts/order_delete.html',context)



