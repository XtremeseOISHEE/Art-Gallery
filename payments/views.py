from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order
from .models import Transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import uuid

@login_required
def initiate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        method = request.POST.get('method')  # 'bkash', 'paypal', 'card', 'cod'
        trx_id = str(uuid.uuid4())  # Random for now, can be replaced with actual gateway ID

        Transaction.objects.create(
            order=order,
            method=method,
            transaction_id=trx_id,
            amount=order.total_price,
            status='success' if method != 'cod' else 'pending',  # COD is pending by nature
        )

        if method != 'cod':
            order.is_paid = True
            order.save()

        messages.success(request, 'Payment processed successfully!')
        return redirect('order_detail', pk=order.id)  # update as needed

    return render(request, 'payments/initiate_payment.html', {'order': order})
