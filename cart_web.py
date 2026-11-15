# Dynamic E-Commerce Cart

# Product database: product name -> price per unit
products = {
    "laptop": 50000,
    "mouse": 500,
    "keyboard": 1200,
    "headphones": 2000,
    "pen": 10,
    "smartphone": 25000,
    "tablet": 18000,
    "monitor": 12000,
    "printer": 8000,
    "usb drive": 600,
    "bluetooth speaker": 1500,
    "earbuds": 2500,
    "microphone": 1800,
    "notebook": 80,
    "marker": 150
}

TAX_RATE = 0.18   # 18% tax

# Discount codes: code -> percent off
coupons = {
    "SAVE10": {
        "discount": 10,
        "min_purchase": 500,
        "max_discount": 1000,
        "description": "Get 10% OFF on purchases above ₹500"
    },

    "SAVE20": {
        "discount": 20,
        "min_purchase": 2000,
        "max_discount": 2000,
        "description": "Get 20% OFF on purchases above ₹2,000"
    },

    "WELCOME15": {
        "discount": 15,
        "min_purchase": 1000,
        "max_discount": 1500,
        "description": "Get 15% OFF on your first purchase (minimum purchase ₹1,000)"
    },

    "FESTIVE25": {
        "discount": 25,
        "min_purchase": 5000,
        "max_discount": 3000,
        "description": "Get 25% OFF on purchases above ₹5,000"
    }
}
applied_discount = 0   # percent currently applied

# Cart is a list of items; each item is a dictionary
cart = []

def show_products():
    print("\nAvailable products:")
    for name in products:
        print(" ", name, "-", products[name])

def add_item():
    name = input("\nEnter product name: ").lower()
    if name in products:
        qty = int(input("Enter quantity: "))
        for item in cart:
            if item["name"] == name:       # already in cart
                item["qty"] = item["qty"] + qty
                print("Quantity updated.")
                return
        cart.append({"name": name, "price": products[name], "qty": qty})
        print(qty, name, "added to cart.")
    else:
        print("Product not found.")

def remove_item():
    name = input("\nEnter product name to remove: ").lower()

    for item in cart:
        if item["name"] == name:
            qty = int(input("Enter quantity to remove: "))

            if qty < item["qty"]:
                item["qty"] -= qty
                print(qty, name, "removed from cart.")
                print("Remaining quantity:", item["qty"])

            elif qty == item["qty"]:
                cart.remove(item)
                print(name, "completely removed from cart.")

            else:
                print("Cannot remove more than the available quantity.")

            return

    print("Item not in cart.")

def apply_coupon():
    global applied_discount
    code = input("\nEnter coupon code: ").upper()
    if code in coupons:
        applied_discount = coupons[code]
        print(applied_discount, "% discount applied.")
    else:
        print("Invalid coupon.")

def show_cart():
    if len(cart) == 0:
        print("\nCart is empty.")
        return
    print("\nYour cart:")
    for item in cart:
        print(" ", item["name"], "x", item["qty"], "=", item["price"] * item["qty"])

def show_total():
    subtotal = 0
    for item in cart:
        subtotal = subtotal + item["price"] * item["qty"]
    discount = subtotal * applied_discount / 100
    after_discount = subtotal - discount
    tax = after_discount * TAX_RATE
    total = after_discount + tax
    print("\nSubtotal:", subtotal)
    print("Discount:", discount)
    print("Tax (18%):", tax)
    print("Total:", total)

# Main menu
while True:
    print("\n1.Show products 2.Add item 3.Remove item 4.View cart 5.Bill 6.Apply coupon 7.Exit")
    choice = input("\nEnter choice: ")

    if choice == "1":
        show_products()
    elif choice == "2":
        add_item()
    elif choice == "3":
        remove_item()
    elif choice == "4":
        show_cart()
    elif choice == "5":
        show_total()
    elif choice == "6":
        apply_coupon()
    elif choice == "7":
        print("Thank you for shopping!")
        break
    else:
        print("Invalid choice.")