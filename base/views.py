from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from base.models import Category, product, ShoppingCart
from base.forms import ProductForm, CatogeryForm, CreateAddtoCartForm
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

