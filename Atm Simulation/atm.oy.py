import datetime
import time  

class ATMMachine:
    def __init__(self):
        # Initialize with a single account for simplicity
        self.accounts = {
            "12345": {
                "pin": "1234",  # PIN for the account
                "balance": 1000,  # Initial balance
                "transactions": []  # List to store transactions
            }
        }
        self.logged_in_account = None  # Store currently logged in account number

    def authenticate(self, acc_num, pin):
        """Check if account exists and if the entered PIN is correct."""
        if acc_num in self.accounts and self.accounts[acc_num]["pin"] == pin:
            self.logged_in_account = acc_num  # Store the account number on successful login
            return True
        else:
            return False

    def get_balance(self):
        """Returns the current balance of the logged-in account."""
        return self.accounts[self.logged_in_account]["balance"]

    def take_out_money(self, amount):
        """Withdraw money from the account, if enough balance exists."""
        if amount > 0 and amount <= self.accounts[self.logged_in_account]["balance"]:
            # Deduct the amount from balance
            self.accounts[self.logged_in_account]["balance"] -= amount
            # Record the transaction with a negative amount for withdrawal
            self._record_transaction("Withdrawal", -amount)
            return True
        else:
            return False

    def put_in_money(self, amount):
        """Deposit money into the account."""
        if amount > 0:
            # Add the amount to the balance
            self.accounts[self.logged_in_account]["balance"] += amount
            # Record the transaction with a positive amount for deposit
            self._record_transaction("Deposit", amount)
            return True
        else:
            return False

    def update_pin(self, new_pin):
        """Update the PIN for the account if the new PIN is valid (4 digits)."""
        if len(new_pin) == 4 and new_pin.isdigit():
            # Update the PIN in the account data
            self.accounts[self.logged_in_account]["pin"] = new_pin
            return True
        else:
            return False

    def show_transaction_history(self):
        """Return the list of transactions for the logged-in account."""
        return self.accounts[self.logged_in_account]["transactions"]

    def _record_transaction(self, trans_type, amount):
        """Record a new transaction (either withdrawal or deposit) with a timestamp."""
        transaction = {
            "type": trans_type,  # Either 'Withdrawal' or 'Deposit'
            "amount": amount,  # Negative for withdrawal, positive for deposit
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp of transaction
        }
        # Append the transaction to the account's history
        self.accounts[self.logged_in_account]["transactions"].append(transaction)

def run_atm():
    atm = ATMMachine()  # Create an instance of ATMMachine
    
    while True:
        print("\n===== Welcome to Bob's ATM =====")
        # Ask for account number and PIN
        account_number = input("Account number, please: ")
        pin = input("Now, your PIN: ")

        # Check if authentication is successful
        if atm.authenticate(account_number, pin):
            print("Login successful! Please wait...")
            time.sleep(1)  # Adding delay for a more realistic experience
            
            while True:
                # Present the main menu options
                print("\nWhat would you like to do?")
                print("1) Check my balance")
                print("2) Get some cash")
                print("3) Make a deposit")
                print("4) Change my PIN")
                print("5) See my recent transactions")
                print("6) I'm done, log me out")
                
                user_choice = input("Enter your choice (1-6): ")
                
                if user_choice == "1":
                    # Option 1: Show current balance
                    print(f"Your current balance is: ${atm.get_balance():.2f}")
                elif user_choice == "2":
                    # Option 2: Withdraw money
                    try:
                        amount = float(input("How much do you want? $"))
                        if atm.take_out_money(amount):
                            print("Here's your cash! Don't spend it all in one place!")
                        else:
                            print("Oops, that didn't work. Check your balance maybe?")
                    except ValueError:
                        print("That's not a valid amount. Try again!")
                elif user_choice == "3":
                    # Option 3: Deposit money
                    try:
                        amount = float(input("How much are you depositing? $"))
                        if atm.put_in_money(amount):
                            print("Thanks for the deposit!")
                        else:
                            print("Hmm, something went wrong. Is it real money?")
                    except ValueError:
                        print("That doesn't look like a number to me. Let's try again.")
                elif user_choice == "4":
                    # Option 4: Change PIN
                    new_pin = input("What's your new secret PIN? ")
                    if atm.update_pin(new_pin):
                        print("PIN updated successfully. Don't forget it!")
                    else:
                        print("PIN update failed. Remember, 4 digits only!")
                elif user_choice == "5":
                    # Option 5: Show transaction history
                    history = atm.show_transaction_history()
                    if history:
                        print("Here's what you've been up to:")
                        # Display each transaction
                        for t in history:
                            print(f"{t['date']} - {t['type']}: ${abs(t['amount']):.2f}")
                    else:
                        print("No transactions yet. Time to start spending!")
                elif user_choice == "6":
                    # Option 6: Log out and return to the start
                    print("Thanks for using Bob's ATM. Come back soon!")
                    break
                else:
                    # Invalid input
                    print("I don't understand that. Let's try again.")
        else:
            # If authentication fails, allow retry
            print("Hmm, that doesn't look right. Wanna give it another shot?")

if __name__ == "__main__":
    run_atm()  # Start the ATM program
