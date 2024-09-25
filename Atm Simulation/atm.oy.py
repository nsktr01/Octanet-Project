import datetime
import time  

class ATMMachine:
    def __init__(self):
        
        self.accounts = {
            "12345": {
                "pin": "1234",
                "balance": 1000,
                "transactions": []
            }
        }
        self.logged_in_account = None

    def authenticate(self, acc_num, pin):
        """Check if account exists and PIN is correct"""
        if acc_num in self.accounts and self.accounts[acc_num]["pin"] == pin:
            self.logged_in_account = acc_num
            return True
        else:
            return False

    def get_balance(self):
        """Shows current balance"""
        return self.accounts[self.logged_in_account]["balance"]

    def take_out_money(self, amount):
        """Take money out of the account"""
        if amount > 0 and amount <= self.accounts[self.logged_in_account]["balance"]:
            self.accounts[self.logged_in_account]["balance"] -= amount
            self._record_transaction("Withdrawal", -amount)
            return True
        else:
            return False

    def put_in_money(self, amount):
        """Put money into the account"""
        if amount > 0:
            self.accounts[self.logged_in_account]["balance"] += amount
            self._record_transaction("Deposit", amount)
            return True
        else:
            return False

    def update_pin(self, new_pin):
        """Update the PIN for the account"""
        if len(new_pin) == 4 and new_pin.isdigit():
            self.accounts[self.logged_in_account]["pin"] = new_pin
            return True
        else:
            return False

    def show_transaction_history(self):
        """Display all transactions for the account"""
        return self.accounts[self.logged_in_account]["transactions"]

    def _record_transaction(self, trans_type, amount):
        """Add a new transaction to the account history"""
        transaction = {
            "type": trans_type,
            "amount": amount,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.accounts[self.logged_in_account]["transactions"].append(transaction)

def run_atm():
    atm = ATMMachine()
    
    while True:
        print("\n===== Welcome to Bob's ATM =====")
        account_number = input("Account number, please: ")
        pin = input("Now, your PIN: ")

        if atm.authenticate(account_number, pin):
            print("Login successful! Please wait...")
            time.sleep(1)  # Added a small delay for realism
            
            while True:
                print("\nWhat would you like to do?")
                print("1) Check my balance")
                print("2) Get some cash")
                print("3) Make a deposit")
                print("4) Change my PIN")
                print("5) See my recent transactions")
                print("6) I'm done, log me out")
                
                user_choice = input("Enter your choice (1-6): ")
                
                if user_choice == "1":
                    print(f"Your current balance is: ${atm.get_balance():.2f}")
                elif user_choice == "2":
                    try:
                        amount = float(input("How much do you want? $"))
                        if atm.take_out_money(amount):
                            print("Here's your cash! Don't spend it all in one place!")
                        else:
                            print("Oops, that didn't work. Check your balance maybe?")
                    except ValueError:
                        print("That's not a valid amount. Try again!")
                elif user_choice == "3":
                    try:
                        amount = float(input("How much are you depositing? $"))
                        if atm.put_in_money(amount):
                            print("Thanks for the deposit!")
                        else:
                            print("Hmm, something went wrong. Is it real money?")
                    except ValueError:
                        print("That doesn't look like a number to me. Let's try again.")
                elif user_choice == "4":
                    new_pin = input("What's your new secret PIN? ")
                    if atm.update_pin(new_pin):
                        print("PIN updated successfully. Don't forget it!")
                    else:
                        print("PIN update failed. Remember, 4 digits only!")
                elif user_choice == "5":
                    history = atm.show_transaction_history()
                    if history:
                        print("Here's what you've been up to:")
                        for t in history:
                            print(f"{t['date']} - {t['type']}: ${abs(t['amount']):.2f}")
                    else:
                        print("No transactions yet. Time to start spending!")
                elif user_choice == "6":
                    print("Thanks for using Bob's ATM. Come back soon!")
                    break
                else:
                    print("I don't understand that. Let's try again.")
        else:
            print("Hmm, that doesn't look right. Wanna give it another shot?")

if __name__ == "__main__":
    run_atm()