from .models import Cart

def cart_context(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Handle anonymous users by creating/retrieving a session-based cart
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    # Group items by (model_id, port_id, start_date, end_date)
    cart_items_grouped = {}
    for item in cart.items.select_related('boat_instance__model', 'boat_instance__port'):
        group_key = f"{item.boat_instance.model.id}_{item.boat_instance.port.id}_{item.start_date}_{item.end_date}"
        if group_key not in cart_items_grouped:
            cart_items_grouped[group_key] = []
        cart_items_grouped[group_key].append(item)

    return {'cart': cart, 'cart_items_grouped': cart_items_grouped}