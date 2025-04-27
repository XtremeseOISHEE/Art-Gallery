from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Order
from artworks.models import Artwork
from .forms import OrderForm

# Helper function to check if user is admin
def is_admin(user):
    return user.is_staff

# Create Order view
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from artworks.models import Artwork

@login_required
def create_order(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)

    # 🔥 New access control
    if request.user.role not in ['buyer', 'seller']:
        messages.error(request, "You are not authorized to place an order.")
        return redirect('artwork_detail', pk=artwork_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.artwork = artwork
            order.total_price = artwork.price * form.cleaned_data['quantity']
            order.save()
            messages.success(request, "Your order has been placed successfully!")
            return redirect('order_list')
        else:
            messages.error(request, "There was an error in your order form. Please try again.")
    else:
        form = OrderForm()

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
