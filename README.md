# ELE 3921 - Pizza Take-Out Project

This is my Django project for a pizza take-out shop. Customers can look at the menu, pick sizes and toppings for pizzas, add stuff to their cart, and then place an order. Admins can use the Django admin panel to change the menu (pizzas, toppings, drinks) and check on all the orders.

## Features:

*   Users can sign up, log in, and log out.
*   Shows a menu where you can pick pizza size & toppings, and drinks.
*   Shopping cart: add items, see your cart, remove items.
*   Lets you place an order.
*   Customers can see their past orders.
*   Admins can manage menu items and orders (and mark orders as done) using the built-in Django admin page.
*   Customers can see if their order is pending or complete.

## Setup:

1.  **Clone it:**
    First, get the code from GitHub (replace `<your-repository-url>` with the actual link!).
    ```bash
    git clone <your-repository-url>
    cd TakeOutPizza
    ```

2.  **Make a virtual environment (Good idea!):**
    This keeps all the Python stuff for this project separate.
    ```bash
    python -m venv venv
    ```
    Then activate it:
    *   Windows: `venv\Scripts\activate`
    *   Mac/Linux: `source venv/bin/activate`

3.  **Install the requirements:**
    Make sure you're in the main `TakeOutPizza` folder (where `requirements.txt` is).
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run database migrations:**
    Go into the `pizzeriaproject` folder (where `manage.py` lives).
    ```bash
    cd pizzeriaproject
    python manage.py migrate
    ```

5.  **Load the sample menu (Optional, but helpful!):**
    This puts the sample pizzas/toppings/drinks into the database so you have a menu to look at.
    Still in the `pizzeriaproject` folder:
    ```bash
    python manage.py loaddata ../data.json
    ```
    (`../data.json` means it expects `data.json` to be in the `TakeOutPizza` folder, one level up from `manage.py`)

6.  **Create an admin user (if you didn't load data or want your own):
**
    Still in `pizzeriaproject`:
    ```bash
    python manage.py createsuperuser
    ```
    It'll ask you for a username, email (optional), and password.

7.  **Start the server:**
    From the `pizzeriaproject` folder:
    ```bash
    python manage.py runserver
    ```

8.  **Check it out in your browser:**
    *   Main site: `http://127.0.0.1:8000/`
    *   Admin panel: `http://127.0.0.1:8000/admin/` (use your superuser login here)

## Test Logins:

(You'll need to fill this in with actual usernames/passwords you create for testing, or explain how to make them if not using the data.json for users)

*   **Admin:**
    *   Username: `[Your Superuser Username]`
    *   Password: `[Your Superuser Password]`
*   **Sample Customer:**
    *   Username: `[A Customer Username you registered]`
    *   Password: `[Their Password]`

## Known Issues / Stuff I Might Add Later:

*   **Images look a bit basic:** Could make the pizza/drink images look cooler or have a gallery.
*   **No real payment:** Obviously, this doesn't actually take your money. Would need to add something like Stripe or PayPal if it were real.
*   **More pizza customization?** Maybe different crust types or special default toppings for some pizzas.
*   **Order tracking map:** Like how Domino's shows your pizza on a map. That would be awesome (but probably super hard).
*   **Forgot password:** Didn't get around to adding a password reset for users.
*   **Responsive design:** It's okay on mobile, but could be much better. Need to learn more CSS for that.
*   Sometimes the session seems a bit sticky if I make big code changes and don't clear cookies. (Student observation) 