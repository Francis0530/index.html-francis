import os
import time

INVENTORY_FILE = "inventory.txt"
USERS_FILE = "users.txt"
SALES_FILE = "sales.txt"

inventory = []
users = {}
sales = []

def hash_password(password):
    return ''.join(str(ord(c) * 2) for c in password)

def save_users():
    with open(USERS_FILE, 'w') as f:
        for username, password in users.items():
            f.write(f"{username} {password}\n")

def load_users():
    users.clear()
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                username, password = line.strip().split()
                users[username] = password

def save_inventory():
    with open(INVENTORY_FILE, 'w') as f:
        for p in inventory:
            f.write(f"{p['id']} {p['name']} {p['quantity']} {p['price']}\n")

def load_inventory():
    inventory.clear()
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r') as f:
            for line in f:
                id_, name, quantity, price = line.strip().split()
                inventory.append({'id': int(id_), 'name': name, 'quantity': int(quantity), 'price': float(price)})

def get_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def save_sales():
    with open(SALES_FILE, 'w') as f:
        for s in sales:
            f.write(f"{s['timestamp']} {s['productId']} {s['productName']} {s['quantitySold']} {s['totalPrice']}\n")

def load_sales():
    sales.clear()
    if os.path.exists(SALES_FILE):
        with open(SALES_FILE, 'r') as f:
            for line in f:
                timestamp, productId, productName, quantitySold, totalPrice = line.strip().split()
                sales.append({
                    'timestamp': timestamp,
                    'productId': int(productId),
                    'productName': productName,
                    'quantitySold': int(quantitySold),
                    'totalPrice': float(totalPrice)
                })

def sign_up():
    username = input("Create username: ")
    password = input("Create password: ")
    if username in users:
        print("Username already taken.")
    else:
        users[username] = hash_password(password)
        save_users()
        print("Account created successfully!")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username in users and users[username] == hash_password(password):
        print("Login successful!")
        return True
    print("Invalid credentials.")
    return False

def add_product():
    id_ = int(input("Enter Product ID: "))
    name = input("Enter Product Name: ")
    quantity = int(input("Enter Quantity: "))
    price = float(input("Enter Price: "))
    inventory.append({'id': id_, 'name': name, 'quantity': quantity, 'price': price})
    save_inventory()
    print("Product added.")

def display_inventory():
    print("\nID\tName\tQuantity\tPrice")
    print("-----------------------------------")
    for p in inventory:
        print(f"{p['id']}\t{p['name']}\t{p['quantity']}\t₱{p['price']:.2f}")

def update_stock():
    id_ = int(input("Enter Product ID to update: "))
    for p in inventory:
        if p['id'] == id_:
            new_quantity = int(input("Enter new quantity: "))
            p['quantity'] = new_quantity
            save_inventory()
            print("Stock updated.")
            return
    print("Product not found.")

def record_sale():
    id_ = int(input("Enter Product ID to sell: "))
    for p in inventory:
        if p['id'] == id_:
            quantity_sold = int(input("Enter quantity sold: "))
            if quantity_sold > p['quantity']:
                print("Not enough stock.")
            else:
                p['quantity'] -= quantity_sold
                sale = {
                    'timestamp': get_timestamp(),
                    'productId': p['id'],
                    'productName': p['name'],
                    'quantitySold': quantity_sold,
                    'totalPrice': quantity_sold * p['price']
                }
                sales.append(sale)
                save_inventory()
                save_sales()
                print("Sale recorded.")
            return
    print("Product not found.")

def check_low_stock():
    threshold = int(input("Enter low stock threshold: "))
    print("\nLow Stock Products:")
    for p in inventory:
        if p['quantity'] <= threshold:
            print(f"{p['name']}: {p['quantity']} units left.")

def generate_summary_report():
    print("\nInventory Summary Report:")
    print("-----------------------------------")
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | Quantity: {p['quantity']} | Price: ₱{p['price']:.2f}")

def generate_sales_report():
    load_sales()
    if not sales:
        print("No sales recorded.")
        return
    total_revenue = 0
    print("\nSales Report:")
    print("-----------------------------------------------------")
    print("Date & Time\tProduct ID\tProduct Name\tQty Sold\tTotal Price")
    for s in sales:
        print(f"{s['timestamp']}\t{s['productId']}\t{s['productName']}\t{s['quantitySold']}\t₱{s['totalPrice']:.2f}")
        total_revenue += s['totalPrice']
    print("-----------------------------------------------------")
    print(f"Total Revenue: ₱{total_revenue:.2f}")

def authentication_menu():
    load_users()
    while True:
        print("\nStockMate: Crochet Business Inventory System")
        print("1. Sign Up\n2. Log In\n3. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            sign_up()
        elif choice == '2':
            if login():
                return
        elif choice == '3':
            print("Exiting...")
            exit()
        else:
            print("Invalid choice.")

def main_menu():
    load_inventory()
    load_sales()
    while True:
        print("\nMain Menu")
        print("1. Add Product\n2. Display Inventory\n3. Update Stock\n4. Sell Product\n5. Check Low Stock\n6. Generate Summary Report\n7. Generate Sales Report\n8. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            add_product()
        elif choice == '2':
            display_inventory()
        elif choice == '3':
            update_stock()
        elif choice == '4':
            record_sale()
        elif choice == '5':
            check_low_stock()
        elif choice == '6':
            generate_summary_report()
        elif choice == '7':
            generate_sales_report()
        elif choice == '8':
            print("Thank you for using StockMate!")
            exit()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    authentication_menu()
    main_menu()
