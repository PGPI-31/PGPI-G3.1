from django.shortcuts import get_object_or_404, redirect, render

from cart.models import Cart
from orders.forms import ClientDataForm, PaymentMethodForm
from orders.models import Order, OrderBoat, Cliente, Pago


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
            return redirect('select_payment_method')
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
            return redirect('select_payment_method')
    else:
        form = ClientDataForm()

    return render(request, 'collect_client_data.html', {'form': form})

def select_paymnet_method(request):
    """
    El usuario selecciona si pagará en el sitio o en línea.
    """
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, status='pending').first()
    else:
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id, user=None)

    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['method']

            # Create or update the payment record
            payment, created = Pago.objects.get_or_create(order=order)
            payment.method = payment_method

            if payment_method == 'on_site':
                payment.payment_address = None
                payment.account_number = None
                payment.save()
                order.status = 'pending_payment'
                order.save()
                return redirect('order_complete')
            elif payment_method == 'online':
                payment.save()
                return redirect('online_payment')
    else:
        form = PaymentMethodForm()

    return render(request, 'select_payment_method.html', {'form': form, 'order': order})


def online_payment(request):
    """
    Simula el proceso de pago en línea.
    """
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, status='pending_payment').first()
    else:
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id, user=None)

    return render(request, 'online_payment.html', {'order': order})


def order_complete(request):
    """
    Muestra la pantalla final del pedido
    """
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, status='pending_payment').first()
    else:
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id, user=None)

    payment = order.payments.first()
    client = Cliente.objects.filter(order=order).first()
    items = order.order_boats.select_related('boat')

    context = {
        'order': order,
        'payment': payment,
        'client': client,
        'items': items,
    }
    return render(request, 'order_complete.html', context)