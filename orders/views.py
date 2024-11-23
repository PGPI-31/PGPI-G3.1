from django.shortcuts import get_object_or_404, redirect, render

from cart.models import Cart
from orders.forms import ClientDataForm
from orders.models import Order, OrderBoat, Cliente


def create_order(request):
    """
    Convierte la cesta en un pedido y redirige a la página de datos del cliente.
    """
    # Retrieve the cart
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        user = request.user
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart = get_object_or_404(Cart, session_key=session_key)
        user = None

    if not cart.items.exists():
        # Redirect back if the cart is empty
        return redirect('ver_catalogo')

    # Create the order
    total_price = sum(item.total_price for item in cart.items.all())
    order = Order.objects.create(
        user=user,
        total_price=total_price,
        status='pending',
    )

    # Create OrderBoat entries
    for item in cart.items.all():
        OrderBoat.objects.create(
            order=order,
            boat=item.boat_instance,
            days=item.number_of_days,
            price_per_day=item.price_per_day,
            price=item.total_price,
            start_date = item.start_date,
            end_date = item.end_date
        )

    # Clear the cart
    cart.items.all().delete()
    cart.delete()

    # Store the order ID in the session for anonymous users
    if not user:
        request.session['order_id'] = order.id

    # Redirect to the client data page
    return redirect('collect_client_data')


def collect_client_data(request):
    # Get the order (logged-in or anonymous)
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, status='pending').first()
        if order:
            # Automatically create a Cliente using the logged-in user's data
            Cliente.objects.get_or_create(
                order=order,
                defaults={
                    'name': request.user.name,
                    'surname': request.user.surname,
                    'telephone': request.user.telephone,
                    'email': request.user.email,
                    'address': request.user.address,
                    'dni': request.user.dni,
                    'birthdate': request.user.birthdate,
                }
            )
            return redirect('collect_delivery_data')
    else:
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id, user=None)

    # Handle anonymous client data
    if request.method == 'POST':
        form = ClientDataForm(request.POST)
        if form.is_valid():
            # Save the client data and associate it with the order
            Cliente.objects.create(
                order=order,
                name=form.cleaned_data['name'],
                surname=form.cleaned_data['surname'],
                telephone=form.cleaned_data['telephone'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                dni=form.cleaned_data['dni'],
                birthdate=form.cleaned_data['birthdate'],
            )
            return redirect('collect_delivery_data')
    else:
        form = ClientDataForm()

    return render(request, 'collect_client_data.html', {'form': form})

def collect_delivery_data(request):
    return render(request, 'collect_delivery_data.html')