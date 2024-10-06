import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inquirer
from sqlalchemy.orm import Session
from Database.Models.customer import CustomerAccount, DiscountCode
from Database.db import SessionLocal
import random, string

def apply_discount_code(session: Session, account: CustomerAccount, total_price: float) -> float:
    """
    Validate and apply a discount code. The code can only be used once.
    """
    # Prompt user for discount code
    #questions = [
    #    inquirer.Text('discount_code', message="Enter discount code (if any)")
    #]
    questions = [
        inquirer.List('has_discount', message="Do you have a discount code you would like to use?", choices=['Yes', 'No'])
    ]
    answers = inquirer.prompt(questions)

    if answers['has_discount'] == "No":
        return total_price

    # If the user says "Yes", ask for the discount code
    questions = [
        inquirer.Text('discount_code', message="Please enter your discount code") 
    ]

    answers = inquirer.prompt(questions)

    if answers['discount_code']:
        discount_code_input = answers['discount_code'].strip() 
        print(f"Entered Discount Code: {discount_code_input}")
    else:
        print("No discount code entered.")
        discount_code_input = None
        return total_price


    if discount_code_input:
        # Validate discount code
        discount_code = session.query(DiscountCode).filter_by(code=discount_code_input).first()

        if not discount_code:
            print("Invalid discount code.")
            return total_price
        elif discount_code.is_used:
            print("This discount code has already been used.")
            return total_price
        elif discount_code.customer_account_id != account.customer_account_id:
            print("This discount code is not valid for your account.")
            return total_price
        else:
            # Apply discount to the total amount
            discount_amount = (total_price * (float(discount_code.discount_percentage) / 100))
            total_price -= discount_amount

            # Mark discount code as used
            discount_code.is_used = True
            session.commit()

            print(f"Discount applied! You saved {discount_amount:.2f}.")
            return total_price

    return total_price

def generate_discount_code(session: Session, account: CustomerAccount, discount_percentage: float):
    """
    Generate a random discount code for a specific customer account.
    """
    discount_code_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    discount_code = DiscountCode(code=discount_code_str, discount_percentage=discount_percentage)
    discount_code.customer_account = account  # Associate discount code with the specific account
    session.add(discount_code)
    session.commit()

    print(f"Discount code generated: {discount_code_str} with {discount_percentage}% off for account {account.customer_account_id}.")

# Example usage
#with SessionLocal() as session:
#    account = session.query(CustomerAccount).filter(CustomerAccount.username == 'user1').first()
#    generate_discount_code(session, account, 10)
#    session.close()
