# Create your views here.

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from boats.models import BoatModel, Port

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

def add_to_cart_catalogue(request, model_id):
    if request.method == "POST":
        # Retrieve data from POST request
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        port_id = request.POST.get('dock')

        # Validate the dates
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if end_date <= start_date:
                raise ValueError("La fecha de fin debe ser posterior a la de inicio.")
        except (ValueError, TypeError) as e:
            messages.error(request, f"Fechas inválidas: {e}")
            return redirect('ver_catalogo')

        # Get the port and boat model
        port = get_object_or_404(Port, id=port_id)
        boat_model = get_object_or_404(BoatModel, id=model_id)

        # Check if there is an available boat instance of this model at the port
        available_instance = BoatInstance.objects.filter(
            model=boat_model,
            port=port,
            available=True
        ).exclude(
            cartitem__start_date__lt=end_date,
            cartitem__end_date__gt=start_date,
        ).first()

        if not available_instance:
            messages.error(request, f"No hay barcos {boat_model.name} en {port.name} disponibles para la fecha seleccionada.")
            return redirect(request.META.get('HTTP_REFERER', 'index'))

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Add the item to the cart
        number_of_days = (end_date - start_date).days
        CartItem.objects.create(
            cart=cart,
            boat_instance=available_instance,
            start_date=start_date,
            end_date=end_date,
            number_of_days=number_of_days,
            price_per_day=available_instance.price_per_day,
        )

        messages.success(request, f"{boat_model.name} ha sido añadido a tu cesta.")
        return redirect(request.META.get('HTTP_REFERER', 'index'))

    # If the request is not POST, redirect to catalogue
    return redirect('catalogue')