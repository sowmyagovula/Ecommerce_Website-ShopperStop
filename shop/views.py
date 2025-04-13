from django.shortcuts import render
from .models import Shop_model, Profile
from .forms import ProductForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

# Create your views here.
def products(request):
    makeup_products = Shop_model.objects.filter(category='makeup')
    skincare_products = Shop_model.objects.filter(category='skincare')
    
    user_type = None
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        user_type = user_profile.user_type

    return render(request, 'products.html', {
        'makeup_products': makeup_products,
        'skincare_products': skincare_products,
        'user_type': user_type
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
def product_del(request, tweet_id):
    product = get_object_or_404(Shop_model, pk = tweet_id, user = request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    return render(request, 'product_del.html', {'product':product})

@login_required
def account_details(request):
    user = request.user
    products = Shop_model.objects.filter(user=user)
    context = {
        'user': user,
        'products': products,
        'user_type': user.profile.user_type,  # assuming Profile exists
    }
    return render(request, 'account_details.html')

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


