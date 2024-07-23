from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import ProductForm, ProductSearchForm
from .models import Product, SavedCart
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

def superuser_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_superuser,
        login_url='loginPage'
    )(view_func)
    return decorated_view_func

def homePage(request):
    form = ProductSearchForm()
    query = request.GET.get('query')
    products = Product.objects.none()  
    if query:
        products = Product.objects.filter(name__icontains=query)
    elif request.user.is_authenticated:
        products = Product.objects.filter(user=request.user)
        if not products.exists():
            return render(request, 'main/noitem.html')
    else:
        return render(request, 'main/non_user.html')

    return render(request, 'main/homePage.html', {'product_list': products, 'search_form': form})

@login_required
def addProduct(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product = product_form.save(commit=False)  # Create an instance but don't save to the database yet
            product.user = request.user
            product.save()
            return redirect('homePage') 
    else:
        product_form = ProductForm()  
    
    context = {
        'form': product_form
    }
    return render(request, 'main/addProduct.html', context)

def detailedPage(request, pk):
    product = get_object_or_404(Product, pk = pk)
    return render(request, 'main/detailedPage.html', {'product': product})

@login_required
def productEdit(request, pk):
    product = get_object_or_404(Product, pk = pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
        return redirect('detailed_page', pk = product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'main/productEdit.html', {'form':form})

@login_required
def confirmDelete(request, pk):
    product = get_object_or_404(Product, pk = pk)
    return render(request, 'main/deleteProduct.html', {'product': product})

@login_required
def deleteProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('homePage')
    # return render(request, 'main/deleteProduct.html', {'product':product})

def cartDetails(request):
    cart = request.session.get('cart', {})
    # Calculate total amount from cart items
    total_amount = sum(item['price'] * item.get('quantity', 1) for item in cart.values())
    context = {
        'cart': cart,
        'total_amount': total_amount
    }
    return render(request, 'main/cartDetails.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})
    message = ''

    if str(product_id) in cart:
        if 'quantity' not in cart[str(product_id)]:
            cart[str(product_id)]['quantity'] = 1
        else:
            cart[str(product_id)]['quantity'] +=1
        message = 'Product is already in the cart'
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1
        }
        message = 'Product added to cart'

    request.session['cart'] = cart
    
    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'message': message, 'cart': cart}, status=200)
    else:
        # Handle non-AJAX request here (if needed)
        context = {
            'message': message,
            'cart': cart,
            'product_list': Product.objects.all()  # Assuming you have a product_list context variable
        }
        return render(request, 'main/homePage.html', context)

def delete_from_cart(request, product_id):
    cart = request.session.get('cart',{})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart_list')

def clear_cart(request):
    cart = request.session.get('cart', {})
    cart.clear()
    request.session['cart'] = cart
    return redirect('cart_list')

def update_cart_quantity(request, product_id, action):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if action == 'increase':
            cart[str(product_id)]['quantity'] += 1
        elif action == 'decrease' and cart[str(product_id)]['quantity'] > 1:
            cart[str(product_id)]['quantity'] -= 1

    request.session['cart'] = cart
    return redirect('cart_list')

@login_required
def save_cart(request):
    cart = request.session.get('cart', {})
    if cart:
        SavedCart.objects.create(user=request.user ,cart_data=cart)
    return redirect('cart_list')

@login_required
def view_saved_carts(request):
    saved_carts = SavedCart.objects.filter(user=request.user).order_by('-saved_at')
    return render(request, 'main/saved_cart.html', {'saved_carts': saved_carts})

def view_saved_cart_details(request, saved_cart_id):
    saved_cart = get_object_or_404(SavedCart, id=saved_cart_id)
    total_amount = sum(item['price'] * item['quantity'] for item in saved_cart.cart_data.values())

    context = {
        'saved_cart': saved_cart,
        'total_amount': total_amount,
    }

    return render(request, 'main/save_cart_details.html', context)

