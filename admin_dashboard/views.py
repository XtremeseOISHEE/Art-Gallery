from django.shortcuts import render
from artworks.models import Artwork
from users.models import User
from orders.models import Order
from django.shortcuts import render, get_object_or_404, redirect

def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')  # Only staff can access

    total_users = User.objects.count()
    total_artworks = Artwork.objects.count()
    total_orders = Order.objects.count()
    orders = Order.objects.all()

    context = {
        'total_users': total_users,
        'total_artworks': total_artworks,
        'total_orders': total_orders,
        'orders': orders,
    }
    return render(request, 'admin_dashboard/admin_dashboard.html', context)


def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        return redirect('admin_dashboard')  # Redirect to the admin dashboard

    return render(request, 'admin_dashboard/update_order_status.html', {'order': order})


# def update_order_status(request, order_id):
#     order = get_object_or_404(Order, id=order_id)

#     if request.method == 'POST':
#         new_status = request.POST.get('status')
#         new_refund_status = request.POST.get('refund_status')

#         order.status = new_status

#         if order.is_refunded:  # ✅ Only allow refund_status update if refund was requested
#             order.refund_status = new_refund_status

#         order.save()
#         return redirect('admin_dashboard')

#     return render(request, 'admin_dashboard/update_order_status.html', {'order': order})

def update_refund_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':        
        new_refund_status = request.POST.get('refund_status')
        if order.is_refunded:  # ✅ Only allow refund_status update if refund was requested
            order.refund_status = new_refund_status
        order.save()
        return redirect('admin_dashboard')
    return render(request, 'admin_dashboard/update_refund_status.html', {'order': order})

