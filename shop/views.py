from django.shortcuts import render
from .models import Shop_model, Profile, CartItem, Order, OrderItem
from .forms import ProductForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db.models import F, Sum

# Create your views here.
def products(request):
    makeup_products = Shop_model.objects.filter(category='makeup')
    skincare_products = Shop_model.objects.filter(category='skincare')
    
    user_type = None
    products = None 

    if request.user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=request.user)
            user_type = user_profile.user_type
            if user_type == 'seller':
                    products = Shop_model.objects.filter(user=request.user)
        except Profile.DoesNotExist:
            user_type = None

    return render(request, 'products.html', {
        'makeup_products': makeup_products,
        'skincare_products': skincare_products,
        'user_type': user_type,
        'products': products,
    })

@login_required
def create_product(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.user_type != 'seller':
        return redirect('products')  # Block buyers
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # if user is logged in
            product.save()
            return redirect('products')  # redirect to product page
    else:
        form = ProductForm()
    return render(request, 'productscreateform.html', {'form': form})


@login_required
def product_edit(request, product_id):
    product = get_object_or_404(Shop_model, pk=product_id, user = request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit = False)
            product.user = request.user
            product.save()
            return redirect('products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'productscreateform.html', {'form':form})

@login_required
def product_del(request, product_id):
    product = get_object_or_404(Shop_model, pk = product_id, user = request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    return render(request, 'product_del.html', {'product':product})


@login_required
def account_details(request):
    user = request.user
    
    products = Shop_model.objects.filter(user=user)
    orders = Order.objects.filter(user=user).prefetch_related('items__product')


    context = {
        'user': user,
        'products': products,
        'user_type': user.profile.user_type,
        'orders': orders,
    }
    return render(request, 'account_details.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('products')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            user_type = form.cleaned_data['user_type']
            Profile.objects.create(user=user, user_type=user_type)
            login(request, user)
            return redirect('products')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def cart(request):
    user = request.user
    if request.method == 'POST':
        if 'remove_item_id' in request.POST:
            item_id = request.POST.get('remove_item_id')
            CartItem.objects.filter(id=item_id, user=request.user).delete()
            return redirect('cart')
        elif 'update_item' in request.POST:
    
            item_id = request.POST.get('update_item')
            try:
                cart_item = CartItem.objects.get(id=item_id, user=user)
                new_quantity = int(request.POST.get(f'quantity_{item_id}'))
                cart_item.quantity = new_quantity
                cart_item.save()
            except CartItem.DoesNotExist:
                pass
            return redirect('cart')
    cart_items = CartItem.objects.filter(user=request.user)
    total = cart_items.aggregate(total=Sum(F('quantity') * F('product__price')))['total']
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Shop_model, pk=product_id)

        # Check if item already in cart
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity  # add quantity
        else:
            cart_item.quantity = quantity  # set initial quantity
        cart_item.save()

        return redirect('cart')
    return redirect('products')
    
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('products')

    order = Order.objects.create(user=request.user)
    for cart_item in cart_items:
        print(f"Creating OrderItem: {cart_item.product} x {cart_item.quantity}")
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
        )
    cart_items.delete()
    return render(request, 'checkout.html', {'order': order})