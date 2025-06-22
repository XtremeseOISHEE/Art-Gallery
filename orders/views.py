from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Order
from artworks.models import Artwork
from .forms import OrderForm
from .models import Cart, CartItem

# orders/views.py

from users.views import staff_or_admin_required

# Helper function to check if user is admin
def is_admin(user):
    return user.is_staff

# Create Order view
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from artworks.models import Artwork


# @login_required
# def create_order(request, artwork_id):
#     artwork = get_object_or_404(Artwork, id=artwork_id)

#     if request.user.role not in ['buyer', 'seller']:
#         messages.error(request, "You are not authorized to place an order.")
#         return redirect('artwork_detail', pk=artwork_id)

#     if request.method == 'POST':
#         form = OrderForm(request.POST, artwork=artwork)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user
#             order.artwork = artwork
#             order.size = form.cleaned_data.get('size')
#             order.frame = form.cleaned_data.get('frame') or 'none'
#             order.quantity = form.cleaned_data['quantity']

#             frame_price_map = {
#                 'wood': 300,
#                 'metal': 350,
#                 'acrylic': 250,
#                 'none': 0,
#             }
#             frame_extra = frame_price_map.get(order.frame, 0)
#             order.total_price = (artwork.price + frame_extra) * order.quantity
#             order.save()

#             # If "Place Order" button is clicked, go directly to confirm
#             if 'place_order' in request.POST:
#                 return redirect('order_confirm', order_id=order.id)
#             else:
#                 return redirect('view_cart')
#         else:
#             messages.error(request, "There was an error in your order form. Please try again.")
#     else:
#         form = OrderForm(artwork=artwork)

#     return render(request, 'orders/create_order.html', {'form': form, 'artwork': artwork})

@login_required
def create_order(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)

    if not hasattr(request.user, 'role') or request.user.role not in ['buyer', 'seller']:
        messages.error(request, "You are not authorized to place an order.")
        return redirect('artwork_detail', pk=artwork_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, artwork=artwork)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.artwork = artwork
            order.size = form.cleaned_data.get('size') or ''
            order.frame = form.cleaned_data.get('frame') or 'none'
            order.quantity = form.cleaned_data['quantity']

            frame_price_map = {
                'wood': 300,
                'metal': 350,
                'acrylic': 250,
                'none': 0,
            }
            frame_extra = frame_price_map.get(order.frame, 0)
            order.total_price = (artwork.price + frame_extra) * order.quantity
            order.save()

            if 'place_order' in request.POST:
                return redirect('order_confirm', order_id=order.id)
            else:
                return redirect('view_cart')
        else:
            messages.error(request, "There was an error in your order form. Please try again.")
    else:
        form = OrderForm(artwork=artwork)

    return render(request, 'orders/create_order.html', {'form': form, 'artwork': artwork})


# View Order detail
@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if request.method == 'POST':
        refund_amount = request.POST.get('refund_amount')
        refund_reason = request.POST.get('refund_reason')

        if refund_amount and refund_reason:
            order.is_refunded = True
            order.refund_amount = refund_amount
            order.refund_reason = refund_reason
            order.save()
            messages.success(request, 'Refund request submitted successfully.')
            return redirect('order_detail', pk=order.pk)
        else:
            messages.error(request, 'Please fill out all fields for the refund request.')

    return render(request, 'orders/order_detail.html', {'order': order})

# List Orders for a user
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

# Admin view to update order status
@login_required
@user_passes_test(is_admin, login_url='order_list')
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Admin can access any order

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'completed', 'cancelled']:
            order.status = new_status
            order.save()
            messages.success(request, f"Order status updated to {new_status}.")
            return redirect('order_detail', pk=order.pk)
        else:
            messages.error(request, "Invalid status selected.")

    return render(request, 'orders/update_order_status.html', {'order': order})

# Cancel order view
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, "Order cancelled successfully.")
    else:
        messages.error(request, "Only pending orders can be cancelled.")

    return redirect('order_list')



@login_required
def add_to_cart(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, artwork=artwork)
    if not created:
        cart_item.quantity += 1  # Optional: increase if already in cart
        cart_item.save()

    messages.success(request, f"{artwork.title} has been added to your cart.")
    return redirect('artwork_list')  # or wherever you want to redirect

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    return render(request, 'orders/cart.html', {'items': items})

from django.http import HttpResponseBadRequest

@login_required
def proceed_to_payment(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_items")
        if not selected_ids:
            messages.error(request, "No items selected.")
            return redirect('view_cart')

        cart = get_object_or_404(Cart, user=request.user)
        items = cart.items.filter(id__in=selected_ids)

        total_price = sum(item.get_total_price() for item in items)

        # Optional: Pass selected item IDs via session or context for next step (e.g., confirm or pay)
        request.session['selected_item_ids'] = selected_ids
        request.session['total_price'] = str(total_price)

        return render(request, 'orders/proceed_to_payment.html', {
            'items': items,
            'total_price': total_price,
        })

    return HttpResponseBadRequest("Invalid request method.")

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .models import Cart, Order  # Make sure you import Order and Cart models

@login_required
def finalize_payment(request):
    if request.method == 'POST':
        selected_item_ids = request.session.get('selected_item_ids')
        delivery_name = request.session.get('delivery_name')
        delivery_phone = request.session.get('delivery_phone')
        delivery_address = request.session.get('delivery_address')

        if not selected_item_ids:
            messages.error(request, "No items were selected.")
            return redirect('view_cart')

        cart = get_object_or_404(Cart, user=request.user)
        items = cart.items.filter(id__in=selected_item_ids)

        if not items.exists():
            messages.error(request, "No valid items to finalize.")
            return redirect('view_cart')

        for item in items:
            Order.objects.create(
                user=request.user,
                artwork=item.artwork,
                quantity=item.quantity,
                total_price=item.get_total_price(),
                delivery_name=delivery_name,
                delivery_phone=delivery_phone,
                delivery_address=delivery_address,
            )
            item.delete()  # Remove item from cart

        # Clear session data
        request.session.pop('selected_item_ids', None)
        request.session.pop('delivery_name', None)
        request.session.pop('delivery_phone', None)
        request.session.pop('delivery_address', None)
        request.session.pop('total_price', None)

        return render(request, 'orders/finalize_payment.html')

    return HttpResponseBadRequest("Invalid request method.")


@login_required
def order_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == "POST":
        order.delivery_name = request.POST.get('name')
        order.delivery_phone = request.POST.get('phone')
        order.delivery_address = request.POST.get('address')
        order.save()
        return redirect('initiate_payment', order_id=order.id)

    return render(request, 'orders/order_confirm.html', {'order': order})


  # if you placed it in a separate file

@staff_or_admin_required
def approve_refund(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.is_refunded and order.refund_status == 'pending':
        order.refund_status = 'approved'
        order.save()
        messages.success(request, 'Refund approved successfully.')
    return redirect('order_detail', pk=pk)

@staff_or_admin_required
def reject_refund(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.is_refunded and order.refund_status == 'pending':
        order.refund_status = 'rejected'
        order.save()
        messages.success(request, 'Refund rejected.')
    return redirect('order_detail', pk=pk)

# @login_required
# def cart_order_confirm(request):
#     selected_item_ids = request.session.get('selected_item_ids')
#     total_price = request.session.get('total_price')

#     if not selected_item_ids or not total_price:
#         messages.error(request, "Something went wrong. Please try again.")
#         return redirect('view_cart')

#     cart = get_object_or_404(Cart, user=request.user)
#     items = cart.items.filter(id__in=selected_item_ids)

#     if request.method == "POST":
#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         address = request.POST.get("address")

#         if not all([name, phone, address]):
#             messages.error(request, "Please fill in all delivery details.")
#             return render(request, 'orders/cart_order_confirm.html', {'items': items, 'total_price': total_price})

#         # ✅ Create orders here (moved from finalize_payment)
#         for item in items:
#             Order.objects.create(
#                 user=request.user,
#                 artwork=item.artwork,
#                 quantity=item.quantity,
#                 total_price=item.get_total_price(),
#                 delivery_name=name,
#                 delivery_phone=phone,
#                 delivery_address=address,
#             )
#             item.delete()  # Remove item from cart

#         # Clear session
#         request.session.pop('selected_item_ids', None)
#         request.session.pop('delivery_name', None)
#         request.session.pop('delivery_phone', None)
#         request.session.pop('delivery_address', None)
#         request.session.pop('total_price', None)

#         messages.success(request, "Your order was placed successfully!")
#         return redirect('order_list')  # or redirect to order success page

#     return render(request, 'orders/cart_order_confirm.html', {'items': items, 'total_price': total_price})
from payments.models import Transaction
import uuid  # to generate dummy transaction_id (for now)

@login_required
def cart_order_confirm(request):
    selected_item_ids = request.session.get('selected_item_ids')
    total_price = request.session.get('total_price')

    if not selected_item_ids or not total_price:
        messages.error(request, "Something went wrong. Please try again.")
        return redirect('view_cart')

    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.filter(id__in=selected_item_ids)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        method = request.POST.get("method")  # ✅ selected radio button value

        if not all([name, phone, address, method]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'orders/cart_order_confirm.html', {
                'items': items,
                'total_price': total_price
            })

        for item in items:
            # ✅ Create order
            order = Order.objects.create(
                user=request.user,
                artwork=item.artwork,
                quantity=item.quantity,
                total_price=item.get_total_price(),
                delivery_name=name,
                delivery_phone=phone,
                delivery_address=address,
            )

            # ✅ Create related transaction
            Transaction.objects.create(
                order=order,
                method=method,
                amount=item.get_total_price(),
                status='pending',  # or 'success' if you treat as auto success
                transaction_id=str(uuid.uuid4())  # temporary random ID
            )

            item.delete()  # remove from cart

        # ✅ Clear session
        request.session.pop('selected_item_ids', None)
        request.session.pop('total_price', None)

        messages.success(request, "Your order was placed successfully!")
        return redirect('order_list')

    return render(request, 'orders/cart_order_confirm.html', {
        'items': items,
        'total_price': total_price
    })
