from .models import Product, Order, Category, OrderItem, Userprofile, Invoice
from django.views.generic import ListView
from django.contrib import messages
from .cart import Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .forms import ProductsFrom, CategoryForm, AddtoCartForm, OrderFrom, CouponForm
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.paginator import Paginator
import io
from reportlab.pdfgen import canvas
from django.http import FileResponse
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
import datetime
from datetime import date
import secrets
import qrcode
from PIL import Image
from reportlab.graphics.barcode import code39, code93
from reportlab_qrcode import QRCodeImage
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm

today = date.today()

generate_no = secrets.randbelow(1000000)
generate_no = str(generate_no).zfill(6)



def home(request):

    return render(request, 'pages/home.html')
# -------------------user authenticate section-------------------


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if not request.user.is_superuser:
                return redirect('product_list')
            else:
                return redirect('dashbord_landing')

        else:
            messages.info(request, "Username and password are invalid")
            return redirect('login')
    else:
        return render(request, 'user/login.html')


def singup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username  alreadt exist")
                return redirect('singup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email address is already registered")
                return redirect('singup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'Sucessfully sing up your account')
                return redirect('login')
        else:
            messages.info(request, "password is invalid")
            return redirect('singup')
    else:
        return render(request, 'user/singup.html')


def logout(request):
    auth_logout(request)
    return redirect('/login')

# ----------------user authenticate end section------------------


# -----------Producrts pages section --------------------------------

def product_list(request):

    queryset = Product.objects.all().order_by(
        '-posted_at')[:12]
    context = {

        "object_list": queryset
    }
    return render(request, "pages/product_list.html", context)


def product_detail(request, id):
    cart = Cart(request)
    obj = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = AddtoCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            cart.add(product_id=id,
                     quantity=quantity, update_quantity=False)

            messages.success(request, 'The product was added to the cart')

    else:
        form = AddtoCartForm()

    related_products = Product.objects.filter(
        category=obj.category).exclude(id=id)[:50]
    context = {
        "related_products": related_products,
        "object": obj,
    }
    return render(request, "pages/product_detail.html", context)


def all_products(request):
    cat = Category.objects.all()
    queryset = Product.objects.all()
    context = {
        "cat": cat,
        "object_list": queryset
    }
    return render(request, 'pages/all_products.html', context)


class CatListView(ListView):
    template_name = 'pages/category_list.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'products': Product.objects.filter(category__name=self.kwargs['category']),
            'ct': Category.objects.all()
        }
        return content


def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {
        "category_list": category_list,
    }
    return context


@login_required(login_url="/login")
def cart_detail(request):
    coupon_form = CouponForm(request.POST)
    producst = Product.objects.all()
    cart_item = Cart(request)
    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)
    
    if coupon_form.is_valid():
        coupon = coupon_form.cleaned_data['code']
        discount = coupon.discount

    if remove_from_cart:
        cart_item.remove(remove_from_cart)

        return redirect('cart_detail')

    if change_quantity:
        cart_item.add(change_quantity, quantity, True)

        return redirect('cart_detail')
    else:
        coupon_form = CouponForm()
    return render(request, 'pages/cart.html', {'cart_item': cart_item,
                                               'coupon_form': coupon_form})


@login_required
def user_order(request):
    total_sell = 0
    cart = Cart(request)

       

    if request.method == 'POST':
        for item in cart:
            product = item['product']
            quantity = int(item['quantity'])
            price = product.price * quantity
            
            
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        address = request.POST['address']
        place = request.POST['place']
        phone = request.POST['phone']
        zipcode = request.POST['zipcode']

        order = Order.objects.create(user=request.user, first_name=first_name, last_name=last_name, product=product, price=price, quantity=quantity,
                                     email=email, phone=phone, address=address, zipcode=zipcode, place=place, created_at=today, order_no=generate_no)


        item = OrderItem.objects.create(
                order=order, products=product, price=price, quantity=quantity, user=request.user)
        cart.clear()
        total_sell =  price
        

        # send_mail(
        #     'Thanks for shopping',
        #     'Thanks for your shopping we will info soon after conform the order .',
        #     'yabindra2057@gmail.com',
        #     # [request.user.email]
        #     ['yabindradev@gmail.com']
        # )
        # fail_silenty = False

        return redirect('/order_details')
    return render(request, 'pages/checkout.html', {'cart': cart})

    # return redirect('cart')


# -----------Producrts pages section --------------------------------


# ----------------------------account and user list section --------------


def user_account(request):
    userprofile = Userprofile.objects.filter(user=request.user)
    user = User.objects.filter(user=request.user)
    return render(request, 'pages/account.html', {'user': user})


def user_details(request):
    return render(request, 'user/user_details.html')


def order_details(request):
    order = Order.objects.filter(user=request.user)
    # ordritem = OrderItem.objects.filter(user=request.user)

    context = {'order': order,
            #    'ordritem': ordritem
            }

    return render(request, 'pages/account_order.html', context)


def user_order_delete(request, id):
    user_order_delete = get_object_or_404(Order, id=id)
    user_order_delete.delete()
    return redirect('order_details')


def user_order_detials(request):
    return render(request, 'user/user_all_order.html')
# invoice generate


def generate_invoice(request):

    invoice_data = Order.objects.filter(user=request.user)

    # orderitem = OrderItem.objects.filter(user=request.user)

    buffer = io.BytesIO()
    finename = f"Ourcompanyname_{request.user.username}.pdf"
    c = canvas.Canvas(buffer)

    page_width, page_height = A4
    left = 0.7 * inch
    center = 3.1 * inch

# Calculate the center of the page
    right = page_width / 1.5

# Set the font and font size
    font = "Helvetica-Bold"
    font_size = 12

# Define the header text
    header_left = "Hour Service.inc"

    messages = "\n Thank you for supporting our small business! We really appreciate your purchase and hope you love your new item.  "
    messages1 = "If you have any issues or need any help, please don't hesitate to reach out. Thanks again for your support! "

    header_right = "Customer Details:"

# Define the company detail
    company_email = "info@acme.com"
    company_phone = "123-456-7890"


# Set the font and font size
    c.setFont(font, font_size)


# Draw the company name and details left side
    c.drawString(left, page_height - 0.7 * inch, header_left)
    c.setFont('Helvetica', 10)
    c.drawString(left, page_height - 0.9 * inch, "Kathamandu Nepal")
    c.drawString(left, page_height - 1.1 * inch, f"Email: {company_email}")
    c.drawString(left, page_height - 1.3 *
                 inch, f"Phone: {company_phone}")


# invoice header right side

    c.drawString(right, page_height - left, f"Invoic No. {generate_no }")
    c.drawString(right, page_height - left - 0.2 *
                 inch, f" Issue Date: {today}")

    c.setLineWidth(5)
    c.line(0, page_height - 1.4 * inch - 0.1 * inch,
           page_width, page_height - 1.4 * inch - 0.1 * inch)

    c.setFont(font, font_size)
    c.setFillColor((1, 0, 0))
# Draw the header
    c.drawString(left, page_height - 1.8 * inch, header_left)
    c.setFont('Helvetica', 10)
    c.setFillColor((0, 0, 0))
    c.drawString(left, page_height - 2.0 * inch,
                 messages)
    c.drawString(left, page_height - 2.2 * inch,
                 messages1)


# ----------------------------------------------------------------
# left
    c.setFont(font, 15)
    c.drawString(left, page_height - 3.0 * inch, "BILL TO")
    c.setFont('Helvetica', 10)

    c.drawString(left, page_height - 3.3 * inch, request.user.username)
    c.drawString(left, page_height - 3.5 * inch, request.user.email)
    c.drawString(left, page_height - 3.7 * inch, f"090880980")
    c.drawString(left, page_height - 3.9 * inch, f"Kawauchi Tokusima")
    c.drawString(left, page_height - 4.1 * inch, f"22323, Japan")


# center
    c.setFont(font, 15)
    c.drawString(center, page_height - 3.0 * inch, "SHIP TO")
    c.setFont('Helvetica', 10)

    c.drawString(center, page_height - 3.3 * inch, "Yabindra Bhujel")
    c.drawString(center, page_height - 3.5 * inch, "yabindra@gmail.com")
    c.drawString(center, page_height - 3.7 * inch, f"090880980")
    c.drawString(center, page_height - 3.9 * inch, f"Kawauchi Tokusima")
    c.drawString(center, page_height - 4.1 * inch, f"22323, Japan")


# right
    c.setFont(font, 15)
    c.drawString(right, page_height - 3.0 * inch, "PAYMENT")
    c.setFont('Helvetica', 10)

    c.drawString(right, page_height - 3.3 * inch, "Due Date: 22/12/2022")
    c.drawString(right, page_height - 3.5 * inch, "¥ 20000")

# line

    c.setLineWidth(0)
    c.line(0, page_height - 4.3 * inch - 0.1 * inch,
           page_width, page_height - 4.3 * inch - 0.1 * inch)

# item
    c.setFont(font, 12)
    c.drawString(left, page_height - 4.6 * inch, "ITEM")
    c.setFont('Helvetica', 10)
    c.drawString(left, page_height - 5.1 * inch,
                 "Thank you for supporting our small business")
    c.drawString(left, page_height - 5.7 * inch,
                 "Thank you for supporting our small business")

    c.drawString(left, page_height - 6.3 * inch,
                 "Sub Total:")
    c.drawString(left, page_height - 6.7 * inch,
                 "Tax (included):")
    c.setFont(font, 15)
    c.drawString(left, page_height - 7.5 * inch,
                 "Grand Total:")

# qty
    c.setFont(font, 12)
    c.drawString(4.0 * inch, page_height - 4.6 * inch, "QTY")
    c.setFont('Helvetica', 10)
    c.drawString(4.1 * inch, page_height - 5.1 * inch,
                 "1")
    c.drawString(4.1 * inch, page_height - 5.7 * inch,
                 "1")


# price
    c.setFont(font, 12)
    c.drawString(5.3 * inch, page_height - 4.6 * inch, "PRICE")
    c.setFont('Helvetica', 10)
    c.drawString(5.3 * inch, page_height - 5.1 * inch,
                 "¥ 120")
    c.drawString(5.3 * inch, page_height - 5.7 * inch,
                 "¥ 120")

#  total

    c.setFont(font, 12)
    c.drawString(7.0 * inch, page_height - 4.6 * inch, "TOTAL")
    c.setFont('Helvetica', 10)
    c.drawString(7.0 * inch, page_height - 5.1 * inch,
                 "¥ 120")
    c.drawString(7.0 * inch, page_height - 5.7 * inch,
                 "¥ 120")

    c.drawString(7.0 * inch, page_height - 6.3 * inch,
                 " ¥ 240")
    c.drawString(7.0 * inch, page_height - 6.7 * inch,
                 "8%")
    c.setFont(font, 15)
    c.drawString(7.0 * inch, page_height - 7.5 * inch,
                 " ¥ 240")

# line

    c.setLineWidth(0)
    c.line(0, page_height - 4.7 * inch - 0.1 * inch,
           page_width, page_height - 4.7 * inch - 0.1 * inch)

    c.setLineWidth(0)
    c.line(0, page_height - 5.3 * inch - 0.1 * inch,
           page_width, page_height - 5.3 * inch - 0.1 * inch)

    c.setLineWidth(0)
    c.line(0, page_height - 5.9 * inch - 0.1 * inch,
           page_width, page_height - 5.9 * inch - 0.1 * inch)

    c.setLineWidth(0)
    c.line(0, page_height - 6.9 * inch - 0.1 * inch,
           page_width, page_height - 6.9 * inch - 0.1 * inch)

    c.setLineWidth(1)
    c.line(0, 0, 8.5*inch, 0)

    c.line(0, page_height - 8 * inch - 0.1 * inch,
           page_width, page_height - 8 * inch - 0.1 * inch)

    invoice = Invoice.objects.create(
        invoice_no=generate_no,  invoice_date=today, customer_name=request.user.username, customer_email=request.user.email)
    invoice.save()
    c.setTitle(finename)
    c.showPage()
    c.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=finename)


# # ----------------------------account and user list section --------------


# -------------------dashbord section------------------------------

def dmain(request):
    user = User.objects.filter(user=request.user)
    user_profile = Userprofile.objects.filter(user=request.user)

    return render(request, 'pages/dmain.html', {'user': user,
                                                'user_profile': user_profile})

# -----dashbord


@login_required(login_url="/login")
def dashbord_landing(request):
    total_order = Order.objects.count()
    total_user = User.objects.count()
    total_products = Product.objects.count()
    
    return render(request, 'dashbord/dashbord_landing.html', {
        'total_order': total_order,
        'total_user': total_user,
        'total_products': total_products,
    })


@login_required(login_url="/login")
def dashbord_order(request):
    new = Order.objects.filter(staus = "Ordered").values().count()
    shiped = Order.objects.filter(staus="Shipped").values().count()
    deleverd = Order.objects.filter(staus="Delivered").values().count()

    
    total_order = Order.objects.count()
    order = Order.objects.all()
    # orderitem = OrderItem.objects.all()

    paginator = Paginator(order, 12)

    page = request.GET.get('page')
    order = paginator.get_page(page)

    context = {'order': order,
               'total_order': total_order,
               'order': order,
               'new': new,
               'shiped':shiped,
               'deleverd':deleverd,
               }

    return render(request, 'dashbord/order.html', context)


def new_order(request):
    new = Order.objects.filter(staus="Ordered").values().count()
    shiped = Order.objects.filter(staus="Shipped").values().count()
    deleverd = Order.objects.filter(staus="Delivered").values().count()
    new_order = Order.objects.filter(staus="Ordered").values()
    
    paginator = Paginator(new_order, 12)

    page = request.GET.get('page')
    new_order = paginator.get_page(page)

    return render(request, 'dashbord/new_order.html', {'new_order': new_order,
                                                       'new':new,
                                                       'shiped':shiped,
                                                       'deleverd': deleverd
                                                       })


def shipped_order(request):
    new = Order.objects.filter(staus="Ordered").values().count()
    shiped = Order.objects.filter(staus="Shipped").values().count()
    deleverd = Order.objects.filter(staus="Delivered").values().count()
    shipped_order = Order.objects.filter(staus="Shipped").values()
    
    paginator = Paginator(shipped_order, 12)

    page = request.GET.get('page')
    shipped_order = paginator.get_page(page)

    return render(request, 'dashbord/shipped_order.html', {'shipped_order': shipped_order,
                                                           'new': new,
                                                           'shiped': shiped,
                                                           'deleverd': deleverd
                                                       })
    
    
def delivered_order(request):
    new = Order.objects.filter(staus="Ordered").values().count()
    shiped = Order.objects.filter(staus="Shipped").values().count()
    deleverd = Order.objects.filter(staus="Delivered").values().count()
    delivered_order = Order.objects.filter(staus="Delivered").values()
    
    
    paginator = Paginator(delivered_order, 12)

    page = request.GET.get('page')
    delivered_order = paginator.get_page(page)
    
    
    return render(request, 'dashbord/delivered.html', {'delivered_order': delivered_order,
                                                       'new': new,
                                                       'shiped': shiped,
                                                       'deleverd': deleverd
                                                           })

def order_details_admin(request, id):
    order_item = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        order_from = OrderFrom(request.POST, instance=order_item)
        if order_from.is_valid():
            order_item = order_from.save(commit=False)
            order_item.save()
            messages.success(request, f'{id} order has been updated.')
            return redirect('dashbord_order')
    else:
        form = OrderFrom(instance=order_item)
        return render(request, 'dashbord/order_details.html', {'form': form,
                                                               'order_item': order_item})


@login_required(login_url="/login")
def generate_shipping_lable(request):
    order = get_object_or_404(Order)
    customer_address = f"{order.order_no} {order.first_name}  {order.email} {order.phone} {order.address} {order.zipcode}"

    buffer = io.BytesIO()
    finename = (f"{order.order_no}.pdf" )
    c = canvas.Canvas(buffer,pagesize=(240,300) )
    left = 8
    
    c.setFillColor(HexColor('#ba689d'))


    c.setFont('Helvetica', 10)
    c.drawString(left, 280, "Hour Service.oi")
    c.drawString(left, 270, "Tokusima Kawauchi")
    c.drawString(left, 260, "Japan")
    c.drawString(left, 250, "08089897")
    c.drawString(left, 240, "hourservice@gmail.com")
    qr = QRCodeImage('http://127.0.0.1:8000/', size=25 * mm)
    qr.drawOn(    c, 160, 235)


    qr = QRCodeImage(customer_address, size=15 * mm)
    qr.drawOn(c, 170, 190)
    
    c.line(0, 233, 300, 233)


    c.setFillColor(HexColor('#0a0007'))
    c.setFont('Helvetica-Bold', 10)
    c.drawString(left, 220, "SHIP TO:")
    c.setFont('Helvetica', 10)
    c.drawString(11, 210, order.first_name)
    c.drawString(11, 200, order.email)
    c.drawString(11, 190, order.phone)
    c.drawString(11, 180, order.address)
    c.drawString(11, 170, order.zipcode)
    barcode_no = order.order_no
    barcode = code39.Extended39(barcode_no, barWidth=0.4*mm, barHeight=11*mm)
    barcode.drawOn(c, 1, 130)
    
    c.setFont('Helvetica-Bold', 10)


    c.drawString(11, 104, "Order No.")
    c.setFont('Helvetica', 10)
    c.drawString(11, 95, barcode_no)

    c.setFont('Helvetica-Bold', 10)
    c.drawString(100, 104, "Order Date.")
    c.setFont('Helvetica', 10)
    c.drawString(100, 95, "2023/1/7")

    c.setFont('Helvetica-Bold', 10)
    c.drawString(180, 104, "Shiped Date.")
    c.setFont('Helvetica', 10)
    c.drawString(180, 95, "2023/1/7")

    c.line(0, 80, 300, 80)
    c.setFillColor(HexColor('#ff8100'))
    
    barcode = code93.Extended93(barcode_no, barWidth=0.4*mm, barHeight=10*mm)
    barcode.drawOn(c, 2, 40)
    c.drawString(15, 20, 'Reciver:')
    c.line(15, 18, 140, 18)


    c.setFont('Helvetica', 8)
    c.drawString(155, 5, ' Hour Service.oi')
    
    

    c.setTitle(finename)
    c.showPage()
    c.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=finename)
    


# ---products
def products(request):
    products = Product.objects.all()

    paginator = Paginator(products, 20)

    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'dashbord/products.html', {'products': products})

# ----cretate new products


def create(request):
    pforms = ProductsFrom()
    if request.POST:
        pforms = ProductsFrom(request.POST)
        if pforms.is_valid():
            #  pforms = pforms.save(commit=False)
            pforms.save()
            return redirect('products')
    return render(request, 'pages/create.html', {'pforms': pforms})

#  ---delete products


def product_delete(request, id):
    # if request.POST():
    product_delete = get_object_or_404(Product, id=id)
    product_delete.delete()
    messages.success(request, f'{id} products has deleted.')
    return redirect('products')

    # return render(request, 'pages/product_delete.html')


# --edit category
def product_edit(request, id):
    product_edit = get_object_or_404(Product, id=id)
    if request.method == "POST":
        form = ProductsFrom(request.POST, instance=product_edit)
        if form.is_valid():
            product_edit = form.save(commit=False)
            product_edit.save()
            messages.success(request, f'{id} products has edited.')
            return redirect('products')
    else:
        form = ProductsFrom(instance=product_edit)
    return render(request, 'pages/product_edit.html', {'form': form})


def category(request):
    dcat = Category.objects.all()
    form = CategoryForm()
    if request.POST:
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "successyfully add the category")
    context = {'form': form,
               'cat': dcat
               }
    return render(request, 'pages/category.html', context)


def category_delete_list(request, id):
    category_delete_list = get_object_or_404(Category, id=id)
    category_delete_list.delete()
    return redirect("category")


def category_edit(request, id):
    category_edit = get_object_or_404(Category, id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category_edit)
        if form.is_valid():
            category_edit = form.save(commit=False)
            category_edit.save()

    else:
        form = CategoryForm(instance=category_edit)
    return render(request, 'pages/category.html', {'form': form})


def customer_detiles(request):
    user = User.objects.all()
    return render(request, 'pages/customer.html', {'user': user})

def admin_setting(request):
    return render(request, 'dashbord/setting.html')
# -------------------dashbord end------------------------------


def sell(request):
    pforms = ProductsFrom(request.POST)
    if pforms.is_valid():
        pforms.save()
        return redirect('/')

    return render(request, 'pages/sell.html', {'pforms': pforms})


# --------------------user informaction------------------------
def user_informaction(request):
    user_address = CustomerForm()
    if request.POST:
        user_address = CustomerForm(request.POST)
        if user_address.is_valid():
            user_address.save()
            return redirect('/')
    return render(request, 'pages/user_profile.html', {'user_address': user_address})


@login_required(login_url="/login")
def help(request):
    return render(request, 'pages/help.html')


# send order conformaction email


# def send_mail(request):
#     # template = render_to_string('email/email.html', )
#     emali = EmailMessage(
#         'Thanks for shopping',
#         'template',
#         'yabindra2057@gmail.com',
#         # [request.user.profile.first_name]
#         ['yabindradev@gmail.com']
#     )
#     emali.fail_silenty = True
#     emali.send()
