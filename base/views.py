from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from base import models
from base.models import Category, ShoppingOrder, product, ShoppingCart, DeliveryAddress
from base.forms import ProductForm, CatogeryForm, CreateAddtoCartForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):
    products = product.objects.all()
    context_dict = {
        'products':products
    }
    return render(request,'home.html',context_dict)


def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/product/form')
    else:
        form = ProductForm()
        context_dict ={
        'form':form
        }
        return render(request,'create_product.html',context_dict)

def list_product(request):
    products = product.objects.all()
    context_dict = {
        'products':products
    }
    return render(request,'list_product.html',context_dict)

# Create your category views here.

def create_catogery(request):
    if request.method == "POST":
        form = CatogeryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/category/form/')
    else:
        form = CatogeryForm()
        context_dict ={
        'form':form
        }
        return render(request,'create_category.html',context_dict)

def list_catogery(request):
    categories = Category.objects.all()
    context_dict = {
        'categories': categories
    }
    return render(request,'list_category.html',context_dict)

def deleteCategory(request, pk):
    categories = Category.objects.get(id=pk)
    categories.delete()
    return redirect('/list/category/')

def editCategory(request, pk):
    category_id = Category.objects.get(id=pk)
    form = CatogeryForm(instance=category_id )
    if request.method == "POST":
        form = CatogeryForm(request.POST, instance=category_id )
        if form.is_valid():
            form.save()
            return redirect('/list/category/')
    context = {'form':form}
    return render(request, 'edit-Category.html', context)

def editProduct(request, pk):
    product_id = product.objects.get(id=pk)
    form = ProductForm(instance=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES,instance=product_id)
        if form.is_valid():
            form.save()
            return redirect('/list/product/')
    context = {'form':form}
    return render(request, 'edit-Product.html',context)

def deleteProduct(request,pk):
    Product= product.objects.get(id=pk)
    Product.delete()
    return redirect('/list/product/')

def Addcart(request,product_id):
    try:
        Product = product.objects.get(id=product_id)
    except product.DoesNotExist:
        return HttpResponse("Product not found", status=404)
    if request.method == 'POST':
        form = CreateAddtoCartForm(request.POST)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.user = request.user
            cart_item.product = Product
            cart_item.save()
            return redirect('home') 
    else:
        form = CreateAddtoCartForm()

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'add_tocart.html', context)

def cart_detail(request):
    if request.user.is_authenticated:
        cart_items = ShoppingCart.objects.filter(user=request.user)
    else:
        cart_items = []
        
    for item in cart_items:
        item.total_price = item.quantity * item.product.price

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'cart_detail.html', context)
    
def OrderCheckout(request):
    user = User.objects.get(id=request.user.id)
    items = ShoppingCart.objects.filter(user=user)
    total_amount = 0
    for item in items:
        total_amount = total_amount+((item.quantity)*(item.product.price))
    shop_order = ShoppingOrder(user=user,total_amount=total_amount)
    shop_order.save()
    return redirect(f'payment/{shop_order.id}/')

def make_payment(request,id):
    shop_order = ShoppingOrder.objects.get(id=id)
    if request.method=='POST':
        paid_amount = request.POST['paid_amount']
        payment_mode = request.POST['payment_mode']
        shop_order.paid_amount = paid_amount
        shop_order.payment_mode = payment_mode
        shop_order.save() 
        return redirect(f'/delivery/address/{shop_order.id}/')
    return render(request,'payment.html',{'shop_order':shop_order})

def order_delivery_address(request,id):
    shop_order = ShoppingOrder.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    delivery_address = DeliveryAddress.objects.filter(user = user)
    if request.method=='POST':
        delivery_address = DeliveryAddress.objects.create(user=user,address = request.POST['address'])
        shop_order.address = delivery_address
        shop_order.payment_status = '0'
        shop_order.delivery_status = '0'
        shop_order.save()
        return HttpResponse('<h1>Order Placed Successfully</h1>.<a href="/">Home</a>')
    return render(request,'address.html',{'shop_order':shop_order,'delivery_address':delivery_address})

def place_order(request,id):
    user = User.objects.get(id=request.user.id)
    delivery_address = DeliveryAddress.objects.filter(user = user)[0]
    shop_order = ShoppingOrder.objects.get(id=id)
    shop_order.address = delivery_address
    shop_order.payment_status = '0'
    shop_order.delivery_status = '0'
    shop_order.save()
    return HttpResponse('<h1>Order Placed Successfully</h1>.<a href="/">Home</a>')