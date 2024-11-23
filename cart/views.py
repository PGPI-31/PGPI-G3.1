# Create your views here.

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import BoatInstance, Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, boat_id):
    boat_instance = get_object_or_404(BoatInstance, id=boat_id)
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    
    if start_date and end_date:
        # Convertir las fechas a objetos datetime.date
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            # Calcular número de días y precio total
            number_of_days = (end_date - start_date).days
            if number_of_days <= 0:
                return render(request, 'error.html', {'message': 'La fecha de fin debe ser posterior a la fecha de inicio.'})
            
            total_price = boat_instance.price_per_day * number_of_days
            
            # Obtener o crear el carrito del usuario
            cart, created = Cart.objects.get_or_create(
                user_id=request.user.id,
                defaults={
                    'created_at': datetime.now(),
                    'updated_at': datetime.now(),
                    'start_date': start_date,
                    'end_date': end_date
                }
            )
            
            # Si el carrito ya existe, actualizamos la fecha de actualización y la fecha de inicio y fin
            if not created:
                cart.updated_at = datetime.now()
                cart.start_date = start_date
                cart.end_date = end_date
                cart.save()

            # Verificar si el producto ya está en la cesta
            existing_item = CartItem.objects.filter(cart_id=cart, boat_instance_id=boat_instance).first()
            if existing_item:
                # Si el producto ya está en la cesta, actualizamos los días y el precio total
                existing_item.number_of_days = number_of_days
                existing_item.price_per_day = boat_instance.price_per_day
                existing_item.total_price = total_price
                existing_item.save()
            else:
                # Crear un nuevo elemento en la cesta
                CartItem.objects.create(
                    cart_id=cart.id,
                    boat_instance_id=boat_instance.id,
                    number_of_days=number_of_days,
                    price_per_day=boat_instance.price_per_day,
                    total_price=total_price
                )
        except ValueError:
            return render(request, 'error.html', {'message': 'Formato de fecha inválido.'})
    
    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart_id__user_id=request.user.id)
    cart_item.delete()
    return redirect('mostrar_cesta')

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



