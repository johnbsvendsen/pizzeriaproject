from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import Pizza, Drink, Topping, Order, OrderItem
from decimal import Decimal

# Create your views here.

def register(request):
    # print("Register view hit, method:", request.method) # for debugging signup
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cool, you\'re registered and logged in!")
            # Redirect to a home/menu page after registration
            # We'll need to define a URL name for this page, e.g., 'menu_list' or 'home'
            return redirect('home') # Placeholder, update to actual URL name later
        else:
            # print("Form errors:", form.errors) # help, whats wrong?
            messages.error(request, "Hmm, check the form for errors.")
    else:
        form = UserRegistrationForm()
    return render(request, 'menu/register.html', {'form': form})

# We will use Django's built-in LoginView and LogoutView in urls.py
# No need to define them here unless we want to customize them heavily.

# Basic home view
def home(request):
    # just shows the homepage
    return render(request, 'menu/home.html')

# Menu display view
def menu_list_view(request):
    pizzas = Pizza.objects.all()
    drinks = Drink.objects.all()
    toppings = Topping.objects.all() # for pizza customization
    # print(f"Pizzas: {pizzas.count()}, Drinks: {drinks.count()}, Toppings: {toppings.count()}")
    context = {
        'pizzas': pizzas,
        'drinks': drinks,
        'toppings': toppings,
        'pizza_sizes': Pizza.PIZZA_SIZES # Pass pizza sizes for the template
    }
    return render(request, 'menu/menu_list.html', context)

@login_required
def add_to_cart_view(request):
    # print("Add to cart request POST:", request.POST)
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item_type = request.POST.get('item_type')
        quantity = int(request.POST.get('quantity', 1)) # Make sure quantity is at least 1

        cart = request.session.get('cart', {})
        # print("Current cart:", cart)
        cart_item_key = None
        item_details = {}

        if item_type == 'pizza':
            pizza = get_object_or_404(Pizza, id=item_id) # FIXME: what if pizza id is weird string? (covered by get_object_or_404)
            size = request.POST.get('size')
            selected_topping_ids = request.POST.getlist('selected_toppings')
            
            if size == 'S':
                unit_price = pizza.base_price_small
            elif size == 'M':
                unit_price = pizza.base_price_medium
            elif size == 'L':
                unit_price = pizza.base_price_large
            else:
                messages.error(request, "Whoops, bad pizza size.")
                return redirect('menu_list')

            toppings_on_pizza = []
            for topping_id in selected_topping_ids:
                topping = get_object_or_404(Topping, id=topping_id)
                if size == 'S':
                    topping_price = topping.price_small
                    unit_price += topping_price
                    toppings_on_pizza.append({'id': topping.id, 'name': topping.name, 'price': str(topping_price)})
                elif size == 'M':
                    topping_price = topping.price_medium
                    unit_price += topping_price
                    toppings_on_pizza.append({'id': topping.id, 'name': topping.name, 'price': str(topping_price)})
                elif size == 'L':
                    topping_price = topping.price_large
                    unit_price += topping_price
                    toppings_on_pizza.append({'id': topping.id, 'name': topping.name, 'price': str(topping_price)})
            
            cart_item_key = f"pizza_{pizza.id}_{size}_{'_'.join(sorted(selected_topping_ids))}"
            item_details = {
                'type': 'pizza',
                'id': pizza.id,
                'name': pizza.name,
                'size': size,
                'size_display': dict(Pizza.PIZZA_SIZES).get(size),
                'selected_toppings': toppings_on_pizza,
                'unit_price': str(unit_price), # Store as string for session serialization
            }

        elif item_type == 'drink':
            drink = get_object_or_404(Drink, id=item_id)
            unit_price = drink.price
            cart_item_key = f"drink_{drink.id}"
            item_details = {
                'type': 'drink',
                'id': drink.id,
                'name': drink.name,
                'unit_price': str(unit_price), # Store as string for session serialization
            }
        else:
            messages.error(request, "Huh? Weird item type.")
            return redirect('menu_list')

        if cart_item_key:
            if cart_item_key in cart:
                updated_quantity = cart[cart_item_key]['quantity'] + quantity
                cart[cart_item_key] = item_details
                cart[cart_item_key]['quantity'] = updated_quantity
            else:
                cart[cart_item_key] = item_details
                cart[cart_item_key]['quantity'] = quantity
            
            cart[cart_item_key]['total_price'] = str(Decimal(cart[cart_item_key]['unit_price']) * cart[cart_item_key]['quantity'])
            
            request.session['cart'] = cart
            request.session.modified = True # Make sure session is saved
            item_name_for_message = item_details.get('name', 'Item') 
            messages.success(request, f"{item_name_for_message} now in your cart!")
            # print("Cart after update:", request.session.get('cart'))
        
        return redirect('menu_list')
    else:
        # Redirect GETs or other methods
        return redirect('menu_list')

@login_required
def remove_from_cart_view(request):
    if request.method == 'POST':
        cart_item_key = request.POST.get('cart_item_key')
        cart = request.session.get('cart', {})

        if cart_item_key in cart:
            item_name = cart[cart_item_key].get('name', 'Item') 
            del cart[cart_item_key]
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, f"Removed {item_name} from your cart.")
        else:
            messages.error(request, "Can\'t find that in your cart (maybe it\'s gone?).")
        
        return redirect('view_cart')
    else:
        return redirect('view_cart') # only POST allowed

@login_required
def place_order_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart\'s empty! Add some pizza first.")
        return redirect('view_cart')

    order_total_price = sum(Decimal(item['total_price']) for item in cart.values())
   
    # order_total_price_alt = Decimal('0.00')
    # for item_val in cart.values():
    # order_total_price_alt += Decimal(item_val['total_price'])

    order = Order.objects.create(user=request.user, total_price=order_total_price)

    for cart_item_key, item_data in cart.items():
        price_at_purchase = Decimal(item_data['unit_price'])
        quantity = item_data['quantity']

        if item_data['type'] == 'pizza':
            pizza = get_object_or_404(Pizza, id=item_data['id'])
            order_item = OrderItem.objects.create(
                order=order,
                pizza=pizza,
                quantity=quantity,
                size=item_data['size'],
                price_at_purchase=price_at_purchase
            )
            if 'selected_toppings' in item_data and item_data['selected_toppings']:
                topping_ids = [topping['id'] for topping in item_data['selected_toppings']]
                toppings = Topping.objects.filter(id__in=topping_ids)
                order_item.selected_toppings.set(toppings)
        
        elif item_data['type'] == 'drink':
            drink = get_object_or_404(Drink, id=item_data['id'])
            OrderItem.objects.create(
                order=order,
                drink=drink,
                quantity=quantity,
                price_at_purchase=price_at_purchase
            )
    
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True # good to be sure

    messages.success(request, "Order placed! Nice.")
    return redirect('order_history')

@login_required
def view_cart_view(request):
    cart = request.session.get('cart', {})
    cart_total = sum(Decimal(item['total_price']) for item in cart.values())
    # print("Viewing cart, total:", cart_total)
    return render(request, 'menu/view_cart.html', {'cart': cart, 'cart_total': cart_total})

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at') # get newest first
    # print("User orders count:", orders.count())
    return render(request, 'menu/order_history.html', {'orders': orders})
