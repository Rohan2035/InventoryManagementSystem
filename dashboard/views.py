from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderMessage
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
from user.models import profile



# Basic Funtions 

@login_required()
def index(request):

    order_b = Order.objects.all()
    product_c = Product.objects.all()
    
    order_s = order_b.count()
    staff_w = User.objects.all().count()
    product_c1 = product_c.count()

    # Flash Message
    global flash_message

    flash_message = False
    
    if OrderMessage.objects.all().exists():
        
        flash_message = OrderMessage.objects.all()[:3]
        

    if request.method == 'POST':

        form = OrderForm(request.POST)

        ordered_quantity = int(form['quantity'].value())
    
            
        if form.is_valid():
                
            ordered_product = form.cleaned_data['product']

            product_ordered = Product.objects.get(name = ordered_product)

            instance = form.save(commit=False)
            instance.staff = request.user

            # Check for the stock
            balance =  product_ordered.quantity - ordered_quantity

            if balance > 0:

                instance.out = False
                product_ordered.quantity = balance
                product_ordered.save()

            else:
                
                messages.warning(request, f'Product {ordered_product} is out of stock hence it\'ll take time for product dispatch. Click on CANCEL to cancel order')
                
                msg = f'{ordered_product} ordered by {request.user} is out of stock'

                o_msg = OrderMessage(name = request.user, invoice = msg)
                o_msg.save()

                instance.out = True


            instance.save()

            return redirect('dashboard-index')

    else:

        form  = OrderForm()
    

    context = {

        'orders' : order_b,
        'products' : product_c,
        'form' : form,

        'w_count' : staff_w,
        'o_count' : order_s,
        'p_count' : product_c1,
        'flash_messages' : flash_message
    
    }

    return render(request, 'dashboard/index.html', context)


@login_required()
def staff(request):

    staff_w = User.objects.all()
    staff_count = staff_w.count()

    order_s = Order.objects.all().count()
    product_s = Product.objects.all().count()

    context = {

        'w' : staff_w,
        'w_count' : staff_count,
        'o_count' : order_s,
        'p_count' : product_s,
        'flash_messages' : flash_message
    }

    return render(request, 'dashboard/staff.html', context)

@login_required()
def staff_detail(request, key):
    
    staff_w = User.objects.get(id = key)

    context = {

        'w' : staff_w
    }

    return render(request, 'dashboard/staff_detail.html', context)


@login_required()
def product(request):
    
    items = Product.objects.all()
    
    staff_w = User.objects.all().count()
    order_s = Order.objects.all().count()
    product_s = items.count()
    
    if request.method == 'POST':
        
        form = ProductForm(request.POST)

        if form.is_valid():
            
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} added to the database')
            return redirect('dashboard-product')

    else:

        form = ProductForm()


    context = {

        'items' : items,
        'form' : form,
        
        'w_count': staff_w,
        'o_count' : order_s,
        'p_count' : product_s,
        'flash_messages' : flash_message,
    }

    return render(request, 'dashboard/product.html', context)


@login_required()
def product_delete(request, key):

    item = Product.objects.get(id = key)
    
    if request.method == 'POST':

        item.delete()
        
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')


@login_required()
def product_update(request, key):

    item = Product.objects.get(id = key)


    if request.method == 'POST':

        form = ProductForm(request.POST, instance=item)

        if form.is_valid():

            product_name = form.cleaned_data["name"]
            p_q = form.cleaned_data["quantity"]
            product_obj = Product.objects.get(name = product_name)
            order_obj = Order.objects.filter(product = product_obj)
            form_post = form.save(commit=False)


            for orders in order_obj:

                if orders.quantity < p_q:

                    p_q = p_q - orders.quantity
                    orders.out = False
                    orders.save()


            form_post.quantity = p_q
            form_post.save()

            return redirect('dashboard-product')

    else:

        form = ProductForm(instance=item)


    context = {

        'form' : form

    }

    return render(request, 'dashboard/product_update.html', context)



@login_required()
def order(request):

    orders_b = Order.objects.all()
    
    staff_w = User.objects.all().count()
    product_s = Product.objects.all().count()
    order_s = orders_b.count()

    context = {

        'orders' : orders_b,
        
        'w_count' : staff_w,
        'o_count' : order_s,
        'p_count' : product_s,
        'flash_messages' : flash_message,

    }

    return render(request, 'dashboard/order.html', context)



# Handler Functions 

@login_required
def dispatch(request, key):
    
    order_dispatch = Order.objects.get(id = key)

    if order_dispatch.out:

        product_balance = Product.objects.get(name = order_dispatch.product.name)

        balance = product_balance.quantity - order_dispatch.quantity

        if balance > 0:

            product_balance.quantity = balance
            product_balance.save()

            order_dispatch.delete()

            messages.success(request, 'Product Sucessfully Dispatched')

        else:

            messages.warning(request, 'Product out of Stock')

    else:

        order_dispatch.delete()
        messages.success(request, 'Product sucessfully Dispatched')

    return redirect('dashboard-order')

@login_required
def delete_order(request, key):
    
    order_delete = Order.objects.get(id = key)
    

    if order_delete.out:

        order_delete.delete()

    else:

        product_update = Product.objects.get(name = order_delete.product.name)

        product_update.quantity += order_delete.quantity

        product_update.save()

        order_delete.delete()

    return redirect('dashboard-index')


# Flash Messages

@login_required
def flash_messages(request):
    
    invoices = OrderMessage.objects.all()

    context = {

        'invoices' : invoices
    }

    return render(request, 'dashboard/flash_messages.html', context)


# Delete Flash Messages
@login_required
def flash_messages_delete(request, key, check):

    if check == 0 and key == 1:
        
        imp_msg = OrderMessage.objects.all()
        imp_msg.delete()
        messages.success(request, 'Successfully Deleted')

    else:

        imp_msg = OrderMessage.objects.get(id = key)
        imp_msg.delete()
        messages.success(request, 'Message Successfully Deleted')

    return redirect('dashboard-flash-messages')

        