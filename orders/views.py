from decimal import Decimal
import json
from venv import logger
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import stripe

from cart.models import Cart
from orders.forms import ClientDataForm, PaymentMethodForm
from orders.models import Order, OrderBoat, Cliente, Pago
from safeport import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from orders.models import StripePayment
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    total_price = cart.get_total_price()
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

    # Store the order ID in the session
    request.session['order_id'] = order.id

    # Redirect to the client data page
    return redirect('collect_client_data')


def collect_client_data(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    # Get the order (logged-in or anonymous)
    if request.user.is_authenticated:
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

def select_payment_method(request):
    """
    El usuario selecciona si pagará en el sitio o en línea.
    """
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

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
                order.status = 'completed'
                order.save()
                base_url = request.build_absolute_uri('/')
                ruta = base_url + '/pedidos/' + str(order.id) + '/'
                send_order_mail(order, ruta)
                return redirect('order_complete')
    else:
        form = PaymentMethodForm()

    return render(request, 'select_payment_method.html', {'form': form, 'order': order})


def online_payment(request):
    """
    Simula el proceso de pago en línea.
    """
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'online_payment.html', {'order': order})


def order_complete(request):
    """
    Muestra la pantalla final del pedido
    """
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

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

def view_order(request, order_id):
    """
    Muestra la pantalla del seguimiento del pedido
    """
    order = get_object_or_404(Order, id=order_id)

    payment = order.payments.first()
    client = Cliente.objects.filter(order=order).first()
    items = order.order_boats.select_related('boat')

    context = {
        'order': order,
        'payment': payment,
        'client': client,
        'items': items,
    }
    return render(request, 'mostrar_pedido.html', context)

@login_required
def list_orders(request):
    """
    Muestra la pantalla de listado de pedidos
    """
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'listar_pedidos.html', {'orders': orders})

def stripe_payment(request):
    """
    Método para pago con stripe
    """
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    payment, created = Pago.objects.get_or_create(order=order)
    payment.method = "online"
    payment.save()

    amount_in_cents = int(Decimal(order.total_price) * 100)
    success_url = request.build_absolute_uri(reverse("payment_success"))
    cancel_url = request.build_absolute_uri(reverse("payment_cancel"))

    # Create a Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": settings.STRIPE_CURRENCY,
                    "product_data": {
                        "name": f'Pedido {order.id}',
                    },
                    "unit_amount": amount_in_cents,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url
    )

    # Save the payment information
    payment = StripePayment.objects.create(
        order=order,
        amount=order.total_price,
        stripe_checkout_session_id=session.id,
        status="pending",
    )

    return JsonResponse({"checkout_url": session.url})


def payment_success(request):
    session_id = request.GET.get("session_id")
    payment = get_object_or_404(StripePayment, stripe_checkout_session_id=session_id)
    payment.status = "completed"
    payment.save()

    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order.status = "completed"
    order.save()

    base_url = request.build_absolute_uri('/')
    ruta = base_url + '/pedidos/' + str(order.id) + '/'
    send_order_mail(order, ruta)

    return redirect('order_complete')

def payment_cancel(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order.status = "cancelled"
    order.save()
    return render(request, "payment_cancel.html")

@csrf_exempt
def cancel_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order_id = data.get('order_id')
        try:
            order = Order.objects.get(id=order_id, status='pending')
            order.status = 'cancelled'
            order.save()
            return JsonResponse({'status': 'success'})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'order_not_found'}, status=404)
    return JsonResponse({'status': 'bad_request'}, status=400)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)  # Invalid payload
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)  # Invalid signature

    # Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        payment = StripePayment.objects.get(stripe_checkout_session_id=session["id"])
        payment.status = "completed"
        payment.save()

    return HttpResponse(status=200)

def send_order_mail(order, ruta):
    """
    Envía el correo de resumen del pedido
    """
    client = Cliente.objects.filter(order=order).first()
    payment = order.payments.first()
    items = order.order_boats.select_related('boat')
    subject = 'Pedido en SafePort realizado correctamente'
    template = get_template('order_mail.html')
    content = template.render({
        'order': order,
        'payment': payment,
        'client': client,
        'items': items,
        'ruta': ruta
    })
    # Configuración del correo
    message = EmailMultiAlternatives(
        subject,  # Asunto del correo
        '',  # Cuerpo del texto plano (opcional)
        settings.EMAIL_HOST_USER,  # Remitente
        [client.email]  # Destinatarios
    )

    # Adjuntar contenido HTML
    message.attach_alternative(content, 'text/html')
    message.send()
