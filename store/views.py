from django.shortcuts import render,HttpResponse
from .models import Customer,SellerAccount,Product,Order,OrderItem,ShippingAddress
from .forms import SignUpForm,SellerAccountForm,addPlantForm
from django.contrib.auth.views import LoginView
from django.shortcuts import reverse,redirect,HttpResponse,render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import CreateView
from random import random
from django.contrib import messages
import datetime
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json
# Create your views here.

# Simplicity function
def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,create = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    return {'cartItems':cartItems,'order':order,'items':items}


# Function for update item in cart
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id = productId)    
    sellerId = product.sellerId
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product,sellerId = sellerId)

    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)

# login function
def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password =request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            
            else:
                messages.info(request, 'Email OR password is incorrect')

        context = {}
        return render(request, 'store/login.html', context)

# logout
def logoutUser(request):
	logout(request)
	return redirect('login')


def store(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        context = {'products':products,'cartItems':cartItems}
    else:
        context = {'products':products,'cartItems':0}
    
    return render(request,'store/store.html',context)

@login_required(login_url='login')
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items,"order":order,"cartItems":cartItems}
    return render(request,'store/cart.html',context)

@login_required(login_url='login')
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items,"order":order,"cartItems":cartItems}
    return render(request,'store/checkout.html',context)


# class for registration and customer registration
class RegisterView(CreateView):
    form_class = SignUpForm
    template_name = 'store/register.html'
    success_url = "/login"

    def form_valid(self,form):
        data = self.request.POST.copy()
        data['username'] = data['email']
        form = SignUpForm(data)
        user = form.save()
        RegisterView.create_profile(user,**form.cleaned_data)
        return super(RegisterView,self).form_valid(form)

    def form_invalid(self,form,**kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
        
    @staticmethod
    def create_profile(user=None,**kwargs):
        customer = Customer.objects.create(user=user,name=kwargs['first_name'] + ' ' + kwargs['last_name'],email=kwargs['email'],phone=kwargs['phone'])
        customer.save()

@login_required(login_url='login')
def registerorg(request):

    if request.method == "POST":
        user = request.user
        email = user.customer.email
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        organization = request.POST.get('organization')
        sellerId= "LP-" + organization[:3].upper() + "-" + "{}".format(int(random()*100))
        seller = SellerAccount.objects.create(name=name,email=email,phone=phone,sellerId=sellerId,organization=organization)
        seller.save()
        user.customer.sellerId = sellerId
        customer = request.user.customer
        customer.save()
        return redirect('/')

    return render(request,'store/register_seller.html')

# for complete taken order
def processOrder(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    total = data['total']
    order.transaction_id = transaction_id
    if float(total) == float(order.get_cart_total):
        order.complete = True
        order.date_ordered = datetime.datetime.now()
    order.save()

    form = ShippingAddress(customer=customer,order=order,address=data['address'],address2 = data['address2'],city=data['city'],state=data['state'],pincode=data['pincode'])
    form.save()
    return JsonResponse("Payment complete!", safe=False)
@login_required(login_url='login')
def dashboard(request):

    
    sellerId = request.user.customer.sellerId
    account = SellerAccount.objects.get(sellerId=sellerId)
    products = Product.objects.filter(sellerId=sellerId)
    # products = Product.objects.filter(SellerAccount=account)
    orders = Order.objects.filter(complete=True)
    items = []
    for order in orders:
        orderitems = OrderItem.objects.filter(order=order)
        for i in orderitems:
            if i.sellerId == sellerId:
                items.append(i)
    pending = 0
    out_for_delivery = 0
    delivered = 0
    total_order = len(items)

    

    if request.method == "POST":
        email = request.POST.get('email')
        product = request.POST.get('product')
        status = request.POST.get('status')

        for i in items:
            if i.order.customer.email == email and i.product.name == product:
                orderitem = OrderItem.objects.get(id = i.id)
                orderitem.status = status
                orderitem.save()

    items = []
    emails = []
    products = []
    for order in orders:
        emails.append(order.customer.email)
        orderitems = OrderItem.objects.filter(order=order)
        for i in orderitems:
            if i.product.name not in products:
                products.append(i.product.name)
            if i.sellerId == sellerId:
                items.append(i)
    
    for i in items:
        if i.status == "Pending":
            pending += 1
        elif i.status == "Out for delivery":
            out_for_delivery +=1
        elif i.status == "Delivered":
            delivered += 1

    context = {'items':items,'pending':pending,'out_for_delivery':out_for_delivery,'delivered':delivered,'total_order':total_order,'emails':emails,
    'products':products}
    return render(request,'store/dashboard.html',context)

@login_required(login_url='login')
def addPlant(request):
    sellerId = request.user.customer.sellerId
    if request.method == "POST":
        data = request.POST.copy()
        data['sellerId'] = sellerId
        form = addPlantForm(data,request.FILES)
        form.save()
        return redirect('/')
        
    else:
        form = addPlantForm()
    context = {'form':form}
    return render(request,'store/addplant.html',context)
 




