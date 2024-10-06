import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inquirer
import threading
import time
from Functionalities.update_status import update_order_status
from Functionalities.status_update_loop import run_status_update_loop
from sqlalchemy.orm import Session
from Database.db import SessionLocal
from InquirerGUI.login_page_inquirer import login_inquirer
from Database.Models.menu import Pizza, Dessert, Drink
from Database.Models.orders import Order
from helper_functions_GUI import print_order_details, log_out, select_free_birthday_drink, select_free_birthday_pizza
from datetime import timedelta, date
from Functionalities.place_order import place_order
from Functionalities.cancel_order import cancel_order
from Functionalities.financial import generate_financial_report


account = None
birthday_offer_homepage = False

# Global reference to track the thread
update_thread = None

def start_GUI(session: Session, account, is_admin) -> None:
    global update_thread

    if update_thread is None or not update_thread.is_alive():
        update_thread = threading.Thread(target=run_status_update_loop, daemon=True)
        update_thread.start()

    while True:
        if is_admin:
            print("\nADMIN HOMEPAGE")
            print(f"Hello {account.customer.first_name} {account.customer.last_name}, welcome to the admin panel of our pizza service!")

            ADMIN_HOMEPAGE_CHOICES = ['View financial report', 'Current Orders', 'View account', 'Log out']
            questions = [
                inquirer.List('action', message="What would you like to do?", choices=ADMIN_HOMEPAGE_CHOICES)
            ]

            answers = inquirer.prompt(questions)

            if answers['action'] == 'View financial report':
                generate_financial_report(session)
            elif answers['action'] == 'Current Orders':
                view_current_orders(session)
            elif answers['action'] == 'View account':
                view_account(session, is_admin)
            elif answers['action'] == 'Log out':
                log_out(session)
                break
        else:
            homepage(session)
            break
            # print("\nHOMEPAGE")
            # print(f"Hello {account.customer.first_name} {account.customer.last_name}, welcome to our pizza service!")

            # HOMEPAGE_CHOICES = ['View account', 'View menu', 'Place order', 'Order history', 'Log out']
            # questions = [
            #    inquirer.List('action', message="What would you like to do?", choices=HOMEPAGE_CHOICES)
            #]

            #answers = inquirer.prompt(questions)

            #if answers['action'] == 'View account':
            #    view_account(session, is_admin)
            #elif answers['action'] == 'View menu':
            #    menu(session)
            #elif answers['action'] == 'Place order':
            #    place_order_page(session)
            #elif answers['action'] == 'Order history':
            #    view_order_history(session)
            #elif answers['action'] == 'Log out':
            #    log_out(session)
            #    break




def homepage(session: Session):
    """
    Homepage for terminal GUI.
    """
    global birthday_offer_homepage
    print("")
    print("HOMEPAGE")
    print(f"Hello {account.customer.first_name} {account.customer.last_name}, welcome to our pizza service!")

    # Check birthday
    today = date.today()
    birthdate = account.customer.birthdate
    if birthdate is not None and birthdate.month == today.month and birthdate.day == today.day:
        if account.birthday_offer_used_year != today.year:
            birthday_offer_homepage = True
        else:
            birthday_offer_homepage = False

    if birthday_offer_homepage:
        print("Happy birthday! You can get a free pizza and drink today!")
        HOMEPAGE_CHOICES = ['GET BIRTHDAY PRESENT', 'View account', 'View menu', 'Place order', 'Order history', 'Log out']
    else:
        HOMEPAGE_CHOICES = ['View account', 'View menu', 'Place order', 'Order history', 'Log out']
    questions = [
        inquirer.List('action', message="What would you like to do?", choices=HOMEPAGE_CHOICES)
    ]

    answers = inquirer.prompt(questions)
    return PAGES[answers['action']](session)

def view_account(session: Session, is_admin: bool=False):
    """
    Show account of customer.
    """
    print("ACCOUNT INFORMATION")
    print(f"Username: {account.username}")
    print(f"Full name: {account.customer.first_name} {account.customer.last_name}")
    print(f"Gender: {account.customer.gender}")
    print(f"Date of birth: {account.customer.birthdate.strftime('%Y-%m-%d')}")
    print(f"Address: {account.customer.address}")
    print(f"Postal Code {account.customer.postal_code}")
    print(f"Amount of previously ordered pizzas: {account.total_pizza_count}")
    if account.discount_pizza_count >= 10:
        print("CONGRATULATIONS, you get a 10% discount on your next order!")


    questions = [
        inquirer.List('action', message="Go back", choices=['To homepage'])
    ]

    answers = inquirer.prompt(questions)

    if is_admin:
        return PAGES['Admin homepage'](session, account, is_admin)
    else:
        return PAGES['To homepage'](session)

def place_order_page(session: Session):
    """
    Show order placement page.
    """
    print("ORDER PLACEMENT")
    if account.discount_pizza_count >= 10:
        print("CONGRATULATIONS, you get a 10% discount on your next order!")

    try:
        # Get all pizzas, drinks, and desserts from the database
        pizzas = session.query(Pizza).all()
        drinks = session.query(Drink).all()
        desserts = session.query(Dessert).all()
    except Exception as e:
        print(f"Error loading pizzas, drinks and desserts: {e}")
        return

    # Option to cancel the order
    cancel_option = ('Cancel order', None)

    # Select pizzas
    pizza_choices = [(pizza.name, pizza) for pizza in pizzas]
    pizza_choices.extend([('Done selecting pizzas', None), cancel_option])

    selected_pizzas = []
    while True:
        questions = [
            inquirer.List('pizza', message="Select at least one pizza to order or 'Done' to finish", choices=[name for name, _ in pizza_choices])
        ]
        answer = inquirer.prompt(questions)

        if answer['pizza'] == 'Cancel order':
            print("ORDER CANCELLED")
            PAGES['To homepage'](session)
            return

        if answer['pizza'] == 'Done selecting pizzas':
            break

        # Get the selected pizza
        selected_pizza = next(pizza for name, pizza in pizza_choices if name == answer['pizza'])

        # Ask for the quantity of the selected pizza
        quantity_question = [
            inquirer.Text('quantity', message=f'How many of pizza {selected_pizza.name} would you like to order?', default='1')
        ]
        quantity_answer = inquirer.prompt(quantity_question)
        quantity = int(quantity_answer['quantity'])

        # Check if pizza is already in selected_pizzas
        found = False
        for i, (pizza, existing_quantity) in enumerate(selected_pizzas):
            if pizza.pizza_id == selected_pizza.pizza_id:
                selected_pizzas[i] = (pizza, existing_quantity + quantity)  # Update quantity if already in list
                found = True
                break

        if not found:
            selected_pizzas.append((selected_pizza, quantity))  # Add new pizza if not already in list

    # Select desserts (optional)
    dessert_choices = [(dessert.name, dessert) for dessert in desserts]
    dessert_choices.extend([('Done selecting desserts', None), cancel_option])

    selected_desserts = []
    while True:
        questions = [
            inquirer.List('dessert', message="Select a dessert to order or 'Done' to finish", choices=[name for name, _ in dessert_choices])
        ]
        answer = inquirer.prompt(questions)

        if answer['dessert'] == 'Cancel order':
            print("ORDER CANCELLED")
            PAGES['To homepage'](session)
            return

        if answer['dessert'] == 'Done selecting desserts':
            break

        # Get the selected dessert
        selected_dessert = next(dessert for name, dessert in dessert_choices if name == answer['dessert'])

        # Ask for the quantity of the selected dessert
        quantity_question = [
            inquirer.Text('quantity', message=f'How many of {selected_dessert.name} would you like to order?', default='1')
        ]
        quantity_answer = inquirer.prompt(quantity_question)
        quantity = int(quantity_answer['quantity'])

        # Check if dessert is already in selected_desserts
        found = False
        for i, (dessert, existing_quantity) in enumerate(selected_desserts):
            if dessert.dessert_id == selected_dessert.dessert_id:
                selected_desserts[i] = (dessert, existing_quantity + quantity)  # Update quantity if already in list
                found = True
                break

        if not found:
            selected_desserts.append((selected_dessert, quantity))  # Add new dessert if not already in list

    # Select drinks (optional)
    drink_choices = [(drink.name, drink) for drink in drinks]
    drink_choices.extend([('Place order', None), cancel_option])

    selected_drinks = []
    while True:
        questions = [
            inquirer.List('drink', message="Select a drink to order or 'Place order' to finish", choices=[name for name, _ in drink_choices])
        ]
        answer = inquirer.prompt(questions)

        if answer['drink'] == 'Cancel order':
            print("ORDER CANCELLED")
            PAGES['To homepage'](session)
            return

        if answer['drink'] == 'Place order':
            break

        # Get the selected drink
        selected_drink = next(drink for name, drink in drink_choices if name == answer['drink'])

        # Ask for the quantity of the selected drink
        quantity_question = [
            inquirer.Text('quantity', message=f'How many of {selected_drink.name} would you like to order?', default='1')
        ]
        quantity_answer = inquirer.prompt(quantity_question)
        quantity = int(quantity_answer['quantity'])

        # Check if drink is already in selected_drinks
        found = False
        for i, (drink, existing_quantity) in enumerate(selected_drinks):
            if drink.drink_id == selected_drink.drink_id:
                selected_drinks[i] = (drink, existing_quantity + quantity)  # Update quantity if already in list
                found = True
                break

        if not found:
            selected_drinks.append((selected_drink, quantity))  # Add new drink if not already in list

    discount_applied = False
    if account.discount_pizza_count >= 10:
        discount_applied = True

    # Place the order
    new_order = place_order(session, account.username, selected_pizzas, selected_drinks, selected_desserts)

    if not new_order:
        print("ORDER CANCELLED")
    else:
        # Order confirmation
        print("ORDER CONFIRMED!\n")
        if discount_applied:
            price_without_discount = round(new_order.total_price / 0.9, 2)
            print(f"Total price without discount: {price_without_discount}")
            print(f"Total price after discount: {new_order.total_price}")
            saved_amount = round(price_without_discount - new_order.total_price, 2)
            print(f"You saved {saved_amount}!\n")
        print(f"Changed your mind? You can cancel your order within 5 minutes of placement, so until {new_order.order_time + timedelta(minutes=5)}")
        print("To cancel your order, select your order on the 'ORDER HISTORY' page and click 'cancel'.\n")

        print_order_details(session, new_order.order_id)
        if account.discount_pizza_count >= 10:
            print("\nCONGRATULATIONS, you get a 10% discount on your next order!")

    # Back to homepage
    questions = [
        inquirer.List('action', message="What would you like to do?", choices=['To homepage', 'Place order'])
    ]
    answers = inquirer.prompt(questions)
    return PAGES[answers['action']](session)

def view_order_history(session: Session):
    """
    Show previous orders of customer, including cancellation option for last order if it is within 5 minutes of placing it.
    """
    print("ORDER HISTORY")
    try:
        # Get a list of previous order IDs for the logged-in customer
        previous_orders = session.query(Order).filter(Order.customer_id == account.customer_id).order_by(Order.order_id.desc()).all()

        if not previous_orders:
            print("You have no previous orders.")
            return PAGES['To homepage'](session)

        # Update the status for all orders
        for order in previous_orders:
            update_order_status(session, order.order_id)  # Update each order's status before displaying

        previous_ids = [p_order.order_id for p_order in previous_orders]
        previous_ids.append('To homepage')

    except Exception as e:
        print(f"Error loading previous order IDs: {e}")
        return PAGES['To homepage'](session)

    questions = [
        inquirer.List('previous_ids', message='These are all your previous orders. Select an order to see more information', choices=previous_ids)
    ]
    answers = inquirer.prompt(questions)

    if answers['previous_ids'] == 'To homepage':
        print("Returning to homepage")
        return PAGES['To homepage'](session)
    else:
        try:
            previous_order = session.query(Order).filter(Order.order_id == answers['previous_ids'], Order.customer_id == account.customer_id).first()

            if not previous_order:
                print("Order not found.")
                return PAGES['Order history'](session)

            if previous_order.birthday_order:
                print("This order was a free birthday present")
            print_order_details(session, previous_order.order_id)
        except Exception as e:
            print(f"Error showing order information: {e}")
            return PAGES['Order history'](session)

        questions = [
            inquirer.List('action', message='What do you want to do', choices=['Cancel order', 'To homepage', 'Order history'])
        ]

        answers = inquirer.prompt(questions)

        if answers['action'] == "To homepage":
            print("Returning to homepage")
            return PAGES['To homepage'](session)
        elif answers['action'] == 'Order history':
            print("Returning to order history")
            return PAGES['Order history'](session)
        elif answers['action'] == 'Cancel order':
            PAGES['Cancel order'](session, previous_order, account)
            return PAGES['To homepage'](session)


def menu(session: Session):
    """
    Menu for terminal GUI.
    """
    print("MENU")
    MENU_ACTIONS = ['View pizzas', 'View drinks', 'View desserts', 'To homepage']
    questions = [
        inquirer.List('action', message="What would you like to do?", choices=MENU_ACTIONS)
    ]

    answers = inquirer.prompt(questions)
    return PAGES[answers['action']](session)

def view_pizzas(session: Session):
    """
    Show list of pizzas. Select pizza to see price, ingredients and diet.
    """
    print("PIZZAS")
    try:
        # Get a list of all pizza names
        pizza_names = [row.name for row in session.query(Pizza.name).all()]
        pizza_names.append('Return to menu')
        pizza_names.append('To homepage')
    except Exception as e:
        print(f"Error loading pizzas: {e}")
        return

    questions = [
        inquirer.List('pizzas', message='These are all the pizzas we offer. Select a pizza to see more information', choices=pizza_names)
    ]

    answers = inquirer.prompt(questions)

    if answers['pizzas'] == 'Return to menu' :
        print("Returning to menu")
        return PAGES['View menu'](session)
    elif answers['pizzas'] == "To homepage":
        print("Returning to homepage")
        return PAGES['To homepage'](session)
    else:
        try:
            # Print pizza information
            selected_pizza = session.query(Pizza).filter(Pizza.name == answers['pizzas']).first()
            print("Pizza " + selected_pizza.name + ":")
            print("    Price: " + str(selected_pizza.price))
            ingredients_list = [pizza_ingredient.ingredient.name for pizza_ingredient in selected_pizza.pizza_ingredients]
            print("    Ingredients: " + ", ".join(ingredients_list))
            if selected_pizza.diet is not None:
                print("    Diet: " + selected_pizza.diet)
        except Exception as e:
            print(f"Error showing pizza information: {e}")
            return

        questions = [
            inquirer.List('turn back', message='Do you want to return to menu or see a different pizza?', choices=['Return to menu', 'To homepage', 'View pizzas'])
        ]

        answers = inquirer.prompt(questions)

        if answers['turn back'] == 'Return to menu':
            print("Returning to menu")
            return PAGES['View menu'](session)
        elif answers['turn back'] == "To homepage":
            print("Returning to homepage")
            return PAGES['To homepage'](session)
        elif answers['turn back'] == 'View pizzas' :
            print("Returning to pizzas")
            return PAGES['View pizzas'](session)

def view_drinks(session: Session):
    """
    Show list of drinks. Select drink to see price.
    """
    print("DRINKS")
    try:
        # Get a list of all drink names
        drink_names = [row.name for row in session.query(Drink.name).all()]
        drink_names.append('Return to menu')
        drink_names.append('To homepage')
    except Exception as e:
        print(f"Error loading drinks: {e}")
        return

    questions = [
        inquirer.List('drinks', message='These are all the drinks we offer. Select a drink to see more information', choices=drink_names)
    ]

    answers = inquirer.prompt(questions)

    if answers['drinks'] == 'Return to menu' :
        print("Returning to menu")
        return PAGES['View menu'](session)
    elif answers['drinks'] == 'To homepage':
        print("Returning to homepage")
        return PAGES['To homepage'](session)
    else:
        try:
            # Print drink information
            selected_drink = session.query(Drink).filter(Drink.name == answers['drinks']).first()
            print("Drink " + selected_drink.name + ":")
            print("    Price: " + str(selected_drink.price))
        except Exception as e:
            print(f"Error showing drink information: {e}")
            return

        questions = [
            inquirer.List('turn back', message='Do you want to return to menu or see a different drink?', choices=['Return to menu', 'To homepage', 'View drinks'])
        ]

        answers = inquirer.prompt(questions)

        if answers['turn back'] == 'Return to menu':
            print("Returning to menu")
            return PAGES['View menu'](session)
        elif answers['turn back'] == 'To homepage':
            print("Returning to homepage")
            return PAGES['To homepage'](session)
        elif answers['turn back'] == 'View drinks' :
            print("Returning to drinks")
            return PAGES['View drinks'](session)

def view_desserts(session: Session):
    """
    Show list of desserts. Select dessert to see price and diet.
    """
    print("DESSERTS")
    try:
        # Get a list of all dessert names
        dessert_names = [row.name for row in session.query(Dessert.name).all()]
        dessert_names.append('Return to menu')
        dessert_names.append('To homepage')
    except Exception as e:
        print(f"Error loading desserts: {e}")

    questions = [
        inquirer.List('desserts', message='These are all the desserts we offer. Select a dessert to see more information', choices=dessert_names)
    ]

    answers = inquirer.prompt(questions)

    if answers['desserts'] == 'Return to menu' :
        print("Returning to menu")
        PAGES['View menu'](session)
    elif answers['desserts'] == "To homepage":
        print("Returning to homepage")
        PAGES['To homepage'](session)
    else:
        try:
            # Print drink information
            selected_dessert = session.query(Dessert).filter(Dessert.name == answers['desserts']).first()
            print("Dessert " + selected_dessert.name + ":")
            print("    Price: " + str(selected_dessert.price))
            if selected_dessert.diet is not None:
                print("    Diet: " + selected_dessert.diet)
        except Exception as e:
            print(f"Error showing dessert information: {e}")

        questions = [
            inquirer.List('turn back', message='Do you want to return to menu or see a different dessert?', choices=['Return to menu', 'To homepage', 'View desserts'])
        ]

        answers = inquirer.prompt(questions)

        if answers['turn back'] == 'Return to menu':
            print("Returning to menu")
            PAGES['View menu'](session)
        elif answers['turn back'] == "To homepage":
            print("Returning to homepage")
            PAGES['To homepage'](session)
        elif answers['turn back'] == 'View desserts' :
            print("Returning to desserts")
            PAGES['View desserts'](session)

def get_birthday_present(session: Session):
    """
    Offer customer a free pizza and drink on their birthday.
    """
    print("CHOOSE A FREE PIZZA AND DRINK FOR YOUR BIRTHDAY!")

    birthday_pizza = select_free_birthday_pizza(session)
    birthday_drink = select_free_birthday_drink(session)

    # Place the order
    new_order = place_order(session, account.username, pizzas=[(birthday_pizza, 1)], drinks=[(birthday_drink, 1)], birthday_offer=True)

    # Order confirmation
    print("ORDER PRESENT CONFIRMED!\n")
    print(f"Changed your mind? You can cancel your present within 5 minutes of placement, so until {new_order.order_time + timedelta(minutes=5)}")
    print("To cancel your present, select your present on the 'ORDER HISTORY' page and click 'cancel'.\n")
    print_order_details(session, new_order.order_id)

    # Back to homepage
    questions = [
        inquirer.List('action', message="What would you like to do?", choices=['To homepage'])
    ]
    answers = inquirer.prompt(questions)
    return PAGES[answers['action']](session)

def view_current_orders(session: Session):
    """
    Display orders that are marked as 'Being prepared' for restaurant monitoring, including pizzas, desserts, and drinks.
    This triggers a status update for each order to ensure real-time accuracy.
    """
    print("CURRENT ORDERS")

    active_orders = session.query(Order).filter(Order.status.in_(["Being prepared", "Out for delivery"])).all()
    for order in active_orders:
        update_order_status(session, order.order_id)

    current_orders = session.query(Order).filter(Order.status == "Being prepared").all()

    if not current_orders:
        print("Currently there are no orders")
    else:
        for order in current_orders:
            print(f"\nOrder ID: {order.order_id}")
            print(f"Customer: {order.customer.first_name} {order.customer.last_name}")
            print(f"Order Time: {order.order_time}")
            print(f"Total Price: {order.total_price}")

            print("PIZZAS ORDERED:")
            for order_pizza in order.order_pizzas:
                print(f"  - {order_pizza.pizza.name} (x{order_pizza.quantity})")

            print("DESSERTS ORDERED:")
            for order_dessert in order.order_desserts:
                print(f"  - {order_dessert.dessert.name} (x{order_dessert.quantity})")

            print("DRINKS ORDERED:")
            for order_drink in order.order_drinks:
                print(f"  - {order_drink.drink.name} (x{order_drink.quantity})")

            print("------")

    questions = [
        inquirer.List('action', message="Go back", choices=['To admin homepage'])
    ]
    answers = inquirer.prompt(questions)
    if answers['action'] == 'To admin homepage':
        return

PAGES = {
    "Login page": login_inquirer,
    "View menu": menu,
    "View pizzas": view_pizzas,
    "View drinks": view_drinks,
    "View desserts": view_desserts,
    "View account": view_account,
    "Place order": place_order_page,
    "Order history": view_order_history,
    "To homepage": homepage,
    "Log out": log_out,
    "Cancel order": cancel_order,
    'GET BIRTHDAY PRESENT': get_birthday_present,
    "Admin homepage": start_GUI
}

with SessionLocal() as session:
    result = login_inquirer(session)  # Assuming login_inquirer returns a tuple

    if result is not None:
        account = result[0]  # Assuming the first item in the tuple is the account object
        # Check if the logged-in account is an admin
        is_admin = account.username == 'admin'  # Adjust this logic as needed
        start_GUI(session, account, is_admin)
    else:
        print("Failed to login or register.")

    session.close()
