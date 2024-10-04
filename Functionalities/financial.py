import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from Database.Models.orders import Order
from Database.Models.customer import Customer
from Functionalities.status_update_loop import run_status_update_loop
import datetime

def generate_financial_report(session: Session):
    """
    Generate a financial report for orders, with filters by gender, age, and postal code.
    """
    # Explicitly refresh the session to ensure it's using the most up-to-date data
    session.expire_all()  # This will expire all objects and ensure fresh data is loaded

    print("Financial Report")

    filters = {
        'gender': input("Filter by gender (M, F, All): ").capitalize(),
        'age': input("Filter by age(-range) (e.g., 18, 26-35, All): "),
        'postal_code': input("Filter by postal code (or All): ")
    }

    query = session.query(Order).join(Customer).filter(Order.status == 'Delivered')

    if filters['gender'] != 'All':
        query = query.filter(Customer.gender == filters['gender'][0])

    age_input = filters['age']

    if age_input != 'All':
        if '-' in age_input:
            age_range = age_input.split('-')
            lower_bound = int(age_range[0])
            upper_bound = int(age_range[1])
            today = datetime.date.today()
            start_date = today - datetime.timedelta(days=365 * upper_bound)
            end_date = today - datetime.timedelta(days=365 * lower_bound)
            query = query.filter(Customer.birthdate.between(start_date, end_date))
        else:
            age = int(age_input)
            today = datetime.date.today()
            birthdate = today - datetime.timedelta(days=365 * age)
            query = query.filter(Customer.birthdate.between(birthdate - datetime.timedelta(days=365), birthdate))

    if filters['postal_code'] != 'All':
        postal_codes = [code.strip() for code in filters['postal_code'].split(',')]
        if len(postal_codes) == 1:
            query = query.filter(Customer.postal_code == postal_codes[0])
        else:
            query = query.filter(Customer.postal_code.in_(postal_codes))

    total_revenue = 0
    order_count = query.count()

    print(f"\nNumber of orders: {order_count}")
    for order in query.all():
        total_revenue += order.total_price
        print(f"Order ID: {order.order_id}, Customer: {order.customer.first_name} {order.customer.last_name}, Price: {order.total_price}")

    print(f"\nTotal Revenue: {total_revenue}\n")
    input("Press enter to return to admin menu.")
