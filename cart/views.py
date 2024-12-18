# Create your views here.

from datetime import datetime
from django.http import Http404
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
            price_per_day=boat_instance.boat__model.price_per_day
        )
        messages.success(request, f"{boat_instance.name} ha sido añadido a tu cesta.")

    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart_id__user_id=request.user.id)
    cart_item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'index'))

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
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "normal":
            request.session['fast'] = False
            cart = get_or_create_cart(request)
            return render(request, 'checkout.html', {'cart': cart})
        elif action == "fast":
            request.session['fast'] = True
            return redirect('create_order')
        else:
            return redirect('ver_catalogo')
    else:
        return redirect('ver_catalogo')

def add_to_cart_catalogue(request, model_id):
    if request.method == "POST":
        # Retrieve data from POST request
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        port_id = request.POST.get('dock')
        quantity = int(request.POST.get('quantity', 1))

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
        available_instances = BoatInstance.objects.filter(
            model=boat_model,
            port=port,
            available=True
        ).exclude(
            order_boats__start_date__lte=end_date,
            order_boats__end_date__gte=start_date,
            order_boats__order__status='completed'
        ).exclude(
            cartitem__start_date__lte=end_date,
            cartitem__end_date__gte=start_date
        )[:quantity]  # Limit to the requested quantity

        if len(available_instances) < quantity:
            messages.error(request, f"No hay suficientes barcos {boat_model.name} en {port.name} disponibles para la fecha seleccionada.")
            return redirect(request.META.get('HTTP_REFERER', 'index'))

        # Get or create the user's cart
        cart = get_or_create_cart(request)

        # Add the item to the cart
        number_of_days = (end_date - start_date).days
        for instance in available_instances:
            CartItem.objects.create(
                cart=cart,
                boat_instance=instance,
                start_date=start_date,
                end_date=end_date,
                number_of_days=number_of_days,
                price_per_day=instance.model.price_per_day,
            )

        messages.success(request, f"{quantity} {boat_model.name}(s) han sido añadidos a tu cesta.")
        return redirect(request.META.get('HTTP_REFERER', 'index'))

    # If the request is not POST, redirect to catalogue
    return redirect('catalogue')

def parse_group_key(group_key):
    try:
        # Split the string using the new delimiter
        parts = group_key.split('_')

        # Ensure the group_key contains exactly 4 parts
        if len(parts) != 4:
            raise ValueError("Group key does not have exactly 4 parts.")

        # Extract components and convert them to their respective data types
        model_id = int(parts[0])
        port_id = int(parts[1])
        start_date = datetime.strptime(parts[2], '%Y-%m-%d').date()
        end_date = datetime.strptime(parts[3], '%Y-%m-%d').date()

        return model_id, port_id, start_date, end_date

    except (ValueError, TypeError):
        # If parsing fails, raise an HTTP 404 error
        raise Http404(f"Invalid group key format: {group_key}")

def get_or_create_cart(request):
    if request.user.is_authenticated:
        # Retrieve or create a cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Retrieve or create a cart for the anonymous session
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def add_quantity(request, group_key):
    cart = get_or_create_cart(request)
    try:
        model_id, port_id, start_date, end_date = parse_group_key(group_key)
    except Http404:
        messages.error(request, "Invalid group key format.")
        return redirect(request.META.get('HTTP_REFERER', 'index'))

    # Get the related objects
    boat_model = get_object_or_404(BoatModel, id=model_id)
    port = get_object_or_404(Port, id=port_id)

    # Check for available instance
    available_instance = BoatInstance.objects.filter(
        model=boat_model,
        port=port,
        available=True
    ).exclude(
        order_boats__start_date__lte=end_date,
        order_boats__end_date__gte=start_date,
        order_boats__order__status='completed'
    ).exclude(
        cartitem__start_date__lt=end_date,
        cartitem__end_date__gt=start_date
    ).first()

    if not available_instance:
        messages.error(request, f"No hay más instancias de {boat_model.name} en {port.name} en la fecha seleccionada.")
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    
    # Add new item
    number_of_days = (end_date - start_date).days
    CartItem.objects.create(
        cart=cart,
        boat_instance=available_instance,
        start_date=start_date,
        end_date=end_date,
        number_of_days=number_of_days,
        price_per_day=boat_model.price_per_day,
    )

    messages.success(request, f"Se ha añadido otro {boat_model.name} a tu cesta.")
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def subtract_quantity(request, group_key):
    cart = get_or_create_cart(request)
    try:
        model_id, port_id, start_date, end_date = parse_group_key(group_key)
    except Http404:
        messages.error(request, "Invalid group key format.")
        return redirect(request.META.get('HTTP_REFERER', 'index'))

    # Find a cart item for the group
    cart_item = CartItem.objects.filter(
        cart=cart,
        boat_instance__model_id=model_id,
        boat_instance__port_id=port_id,
        start_date=start_date,
        end_date=end_date
    ).first()

    if not cart_item:
        messages.error(request, f"No hay elementos a eliminar")
        return redirect(request.META.get('HTTP_REFERER', 'index'))

    # Remove the cart item
    cart_item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def merge_carts(sender, request, user, **kwargs):
    session_cart = Cart.objects.filter(session_key=request.session.session_key).first()
    user_cart = Cart.objects.filter(user=user).first()

    if session_cart:
        if not user_cart:
            # Assign the session cart to the user
            session_cart.user = user
            session_cart.session_key = None
            session_cart.save()
        else:
            # Merge items from session_cart into user_cart
            for item in session_cart.items.all():
                item.cart = user_cart
                item.save()
            session_cart.delete()
