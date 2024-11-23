# Create your views here.

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import BoatInstance, Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, boat_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    boat_instance = get_object_or_404(BoatInstance, id=boat_id)

    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    if not start_date or not end_date:
        messages.error(request, "Please provide both start and end dates.")
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    
    # Calculate number of days
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        number_of_days = (end_date - start_date).days
        if number_of_days <= 0:
            raise ValueError("Fecha de fin debe ser posterior a la de inicio.")
    except ValueError as e:
        messages.error(request, f"Fechas inválidas: {e}")
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    
    # Check if the item already exists in the cart for the same dates
    existing_item = CartItem.objects.filter(
        cart=cart,
        boat_instance=boat_instance,
        start_date=start_date,
        end_date=end_date
    ).first()

    if existing_item:
        messages.info(request, f"{boat_instance.name} ya está en tu cesta.")
    else:
        # Add the new item to the cart
        CartItem.objects.create(
            cart=cart,
            boat_instance=boat_instance,
            start_date=start_date,
            end_date=end_date,
            number_of_days=number_of_days,
            price_per_day=boat_instance.price_per_day
        )
        messages.success(request, f"{boat_instance.name} ha sido añadido a tu cesta.")

    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart_id__user_id=request.user.id)
    cart_item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def checkout(request):
    # Implementación de formalización del alquiler
    return render(request, 'formalizacion.html')

from django.shortcuts import render, get_object_or_404
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def view_cart(request):
    """
    Muestra la cesta del usuario actual.
    Si no existe, la crea al añadir un objeto posteriormente.
    """
    # Buscar la cesta asociada al usuario, pero pasar el ID explícito
    cart = Cart.objects.filter(user_id=request.user.id).first()
    cart_items = CartItem.objects.filter(cart_id=cart) if cart else []
    
    return render(request, 'mostrar_cesta.html', {'cart_items': cart_items})


def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)

    return render(request, 'checkout.html', {'cart': cart})

