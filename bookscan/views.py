from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Products,Author, Cart, ContactDetails, Order
from django.db.models import Sum
from django.db.models import F
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def index(request):
    user_id = request.user.id
    cart_items_len = Cart.objects.filter(user=user_id).aggregate(total_quantity=Sum('quantity'))['total_quantity']
    if not cart_items_len:
        cart_items_len = 0
    context = {}
    context['product_data'] = Products.objects.all()
    context['author_data']=Author.objects.all()
    context['cart_items_len']=cart_items_len
    return render(request, 'pages/home.html', context)

def about_us(request):
    return render(request, 'pages/about.html')


def contact(request):
  print("hiiiiiiiiiiiiiiii")
  if request.method == "POST":
    print(request.POST,"POSTTTTTTTTTTTTTTTT")
    email = request.POST.get("email")
    name = request.POST.get('name')
    message = request.POST.get("message")
   
    ContactDetails.objects.create(email=email, name=name, message=message)
    response = {'message':'Thanks for Contact Us','status':'success'}
    return JsonResponse(response)

@login_required(login_url='login_user')
def cart(request):
    user_id = request.user.id
    cart_data = Cart.objects.filter(user_id=user_id)
    if not cart_data:
        return redirect('home')
    cart_items_len = Cart.objects.filter(user=user_id).aggregate(total_quantity=Sum('quantity'))['total_quantity']
    total_product_price  = Cart.objects.filter(user=user_id).aggregate(total=Sum(F('total_price')))['total']
    if not total_product_price:
        total_product_price = 0.0
    if not cart_items_len:
        cart_items_len = 0
    context = {}
    context['cart_items_len']=cart_items_len
    context['cart_data']=cart_data
    context['total_product_price']=total_product_price
    return render(request, 'pages/cart.html', context)

@login_required(login_url='login_user')
def add_cart(request):
    user_id = request.user.id
    if request.method == "POST":
        cart_id = request.POST['cart_id']
        if Cart.objects.filter(user_id=user_id, item_id=cart_id).exists():
            response = {'message':'cart already created','status':False}
        else:
           product_data = Products.objects.filter(id=cart_id).first()
           total_price = product_data.price * 1
           Cart.objects.create(user_id=user_id, item_id=cart_id, total_price=total_price)
           cart_items_len = Cart.objects.filter(user=user_id).aggregate(total_quantity=Sum('quantity'))['total_quantity']
           response = {'message':'cart created successfully','status':True, 'cart_items_len':cart_items_len} 
    return JsonResponse(response)

@login_required(login_url='login_user')
def remove_cart(request):
    if request.method == "POST":
        user_id = request.user.id
        product_item_id = request.POST['product_item_id']
        delete_cart_data = Cart.objects.filter(id=product_item_id).first()
        delete_cart_data.delete()
        cart_items_len = Cart.objects.filter(user=user_id).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        if not cart_items_len:
            cart_items_len = 0
        total_product_price  = Cart.objects.filter(user=user_id).aggregate(total=Sum(F('total_price')))['total']
        response = {'message':'Cart deleted successfully','status':True,'cart_items_len':cart_items_len,'total_product_price':total_product_price}
    return JsonResponse(response)

@login_required(login_url='login_user')
def update_cart(request):
    if request.method == "POST":
        user_id = request.user.id
        cart_id = int(request.POST['cart_id'])
        input_number = int(request.POST['input_number'])
        total_product_price  = Cart.objects.filter(user=user_id, id=cart_id).aggregate(total=Sum(F('item__price') * F('quantity')))['total']
        cart_data = Cart.objects.filter(id=cart_id).update(quantity=input_number, total_price=float(total_product_price))
        total_product_new_price  = Cart.objects.filter(user=user_id, id=cart_id).aggregate(total=Sum(F('item__price') * F('quantity')))['total']
        cart_items_len = Cart.objects.filter(user=user_id).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        cart_total_product_price  = Cart.objects.filter(user=user_id).aggregate(total=Sum(F('total_price')))['total']
    return JsonResponse({'message':'Cart Updated successfully','status':True,'cart_items_len':cart_items_len,'total_product_price':f'${total_product_new_price}','cart_total_product_price':f'${cart_total_product_price}'})

@login_required(login_url='login_user')
@csrf_exempt
def checkout(request):
    user_id = request.user.id
    product_data = Products.objects.all()
    cart_items_len = Cart.objects.filter(user=user_id).aggregate(total_quantity=Sum('quantity'))['total_quantity']
    total_product_price  = Cart.objects.filter(user=user_id).aggregate(total=Sum(F('total_price')))['total']
    cart_data = Cart.objects.filter(user_id=user_id)
    if not cart_items_len:
            cart_items_len = 0
    context = {}
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name  = request.POST['last_name']
        phone_number = request.POST['phone_number']
        company_name = request.POST['company_name']
        email = request.POST['email']
        town_city = request.POST['town_city']
        state = request.POST['state']
        address_line1 = request.POST['address_line1']
        address_line2 = request.POST['address_line2']
        zip_code = request.POST['zip_code']
        notes = request.POST['notes']
        country = request.POST['country']
        order_data = Order.objects.create(user_id=user_id, price=total_product_price, address_line1=address_line1, address_line2=address_line2, phone_number=phone_number, town_city=town_city, state=state, first_name=first_name, last_name=last_name, company_name=company_name, zipcode=zip_code, country=country, notes=notes, email=email)
        order_data.product.set(product_data)
        delete_cart = Cart.objects.filter(user=user_id).delete()
        response = {'message':'Your Order Successfully','status':'success'}
        return JsonResponse(response)
    context['cart_items_len']=cart_items_len
    context['cart_data']=cart_data
    context['total_product_price']=total_product_price
    return render(request, 'pages/checkout.html', context)



def login_user(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    username = User.objects.get(email=email.lower()).username
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        request.session['user_id'] = user.id
        response = {'message':'User Login Successfully','status':'success'}
    else:
        response = {'message':'Invalid User Detail','status':'fail'}
    return JsonResponse(response)
  return render(request, 'pages/login.html')



def signup_user(request):
  if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        confirm_password = request.POST['confirm_password']
        if len(password) < 7:
                response = {'message': 'Password must contain at least 7 characters.',
                                    'status': 'Error'}
                return JsonResponse(response)
        if password != confirm_password:
                response = {'message': 'password and conform password do not matched',
                                            'status': 'error',}
                return JsonResponse(response)
        myuser = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                            email=email, password=password)
        myuser.save()
        response = {'message': 'Thanks for your Registration user has been created Successfully',
                                            'status': 'success'}
        return JsonResponse(response)
  return render(request, 'pages/signup.html')



def logout(request):
    auth_logout(request)
    return redirect('home')


@login_required
def AddBanner(request):
    b