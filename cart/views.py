# Create your views here.


from django.shortcuts import render, redirect, get_object_or_404
from .models import BoatInstance, Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, boat_id):
    boat_instance = get_object_or_404(BoatInstance, id=boat_id)
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    if start_date and end_date:
        number_of_days = (end_date - start_date).days
        total_price = boat_instance.price_per_day * number_of_days
        cart, created = Cart.objects.get_or_create(user_id=request.user, defaults={})
        CartItem.objects.create(
            cart_id=cart,
            boat_instance_id=boat_instance,
            number_of_days=number_of_days,
            price_per_day=boat_instance.price_per_day,
            total_price=total_price
        )
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart_id__user_id=request.user)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = Cart.objects.filter(user_id=request.user).first()
    cart_items = CartItem.objects.filter(cart_id=cart) if cart else []
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items})

@login_required
def checkout(request):
    # Implementación de finalización del alquiler
    return render(request, 'cart/checkout.html')

