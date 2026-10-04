import csv
import os
from datetime import datetime

DATA_FILE = "expenses.csv"

def initialize_file():
    """Creates the CSV file with headers if it does not exist."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])

def load_expenses():
    """Loads all expenses from the CSV file."""
    expenses = []
    if not os.path.exists(DATA_FILE):
        return expenses
    
    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                row["Amount"] = float(row["Amount"])
                expenses.append(row)
            except ValueError:
                continue
    return expenses

def add_expense():
    """Prompts the user to add a new expense."""
    print("\n--- Add New Expense ---")
    
    # 1. Get Category
    categories = ["Food", "Transport", "Entertainment", "Bills", "Other"]
    print("Categories:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    
    try:
        choice = int(input("Select category number: "))
        if 1 <= choice <= len(categories):
            category = categories[choice - 1]
        else:
            category = "Other"
    except ValueError:
        category = "Other"

    # 2. Get Amount
    while True:
        try:
            amount = float(input("Enter amount spent: "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # 3. Get Description
    description = input("Enter a brief description: ").strip()
    if not description:
        description = "N/A"

    # 4. Get Date
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Save to file
    with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([date_str, category, amount, description])
    
    print(f"✅ Success! Added ₹{amount:.2f} to {category}.")
    check_budget()

def view_expenses():
    """Displays a formatted list of all recorded expenses."""
    expenses = load_expenses()
    if not expenses:
        print("\n📭 No expenses recorded yet.")
        return

    print("\n" + "="*55)
    print(f"{'Date':<12} | {'Category':<15} | {'Amount':<10} | {'Description'}")
    print("="*55)
    
    total = 0.0
    for exp in expenses:
        print(f"{exp['Date']:<12} | {exp['Category']:<15} | ₹{exp['Amount']:<9.2f} | {exp['Description']}")
        total += exp['Amount']
        
    print("="*55)
    print(f"{'TOTAL EXPENSES':<30} | ₹{total:.2f}")
    print("="*55)

def check_budget():
    """Checks total expenses against a user-defined monthly limit."""
    # Default budget limit configuration
    budget_limit = 10000.0 
    expenses = load_expenses()
    current_month = datetime.now().strftime("%Y-%m")
    
    monthly_total = sum(
        exp['Amount'] for exp in expenses if exp['Date'].startswith(current_month)
    )
    
    print(f"📊 Monthly Progress ({current_month}): ₹{monthly_total:.2f} / ₹{budget_limit:.2f}")
    if monthly_total > budget_limit:
        print("⚠️ WARNING: You have exceeded your monthly budget limit!")
    elif monthly_total >= budget_limit * 0.9:
        print("⚠️ ALERT: You have used over 90% of your monthly budget!")

def main():
    initialize_file()
    while True:
        print("\n====== PYTHON EXPENSE TRACKER ======")
        print("1. Add an Expense")
        print("2. View All Expenses")
        print("3. Check Budget Status")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            check_budget()
        elif choice == '4':
            print("\nGoodbye! Happy budgeting! 👋")
            break
        else:
            print("Invalid option. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
