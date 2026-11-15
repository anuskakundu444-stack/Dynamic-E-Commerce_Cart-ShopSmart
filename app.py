import base64
from operator import sub
from pathlib import Path
import streamlit as st
from datetime import datetime
import uuid


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="ShopSmart | Online Store",
    page_icon="ShopSmart.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* =================================
   GENERAL WEBSITE BACKGROUND
================================= */

.stApp {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* =================================
   SIDEBAR
================================= */

[data-testid="stSidebar"] {
    background-color: #ffffff;
}

/* =================================
   HERO SECTION
================================= */

.hero {
    background: linear-gradient(120deg, #172554, #2563eb);
    padding: 35px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 38px;
}

.hero p {
    color: #dbeafe;
    font-size: 16px;
}

/* =================================
   PRODUCT CARDS
================================= */

div[class*="st-key-product_card_"] {
    height: 480px !important;
    min-height: 480px !important;
    box-sizing: border-box;
    overflow: hidden;
    border-radius: 14px;
}

/* =================================
   UNIFORM PRODUCT IMAGES
================================= */

.product-image-box {
    width: 100%;
    height: 180px;
    overflow: hidden;
    border-radius: 10px;
    margin-bottom: 12px;
    background-color: #f8fafc;
}

.product-image-box img {
    display: block;
    width: 100%;
    height: 180px;
    object-fit: cover;
    object-position: center;
    border-radius: 10px;
}

/* =================================
   PRODUCT DESCRIPTION
================================= */

div[class*="st-key-product_card_"] [data-testid="stMarkdownContainer"] p {
    min-height: 45px;
}

/* =================================
   PRODUCT PRICE
================================= */

.product-price {
    color: #2563eb;
    font-size: 23px;
    font-weight: bold;
}

/* =================================
   SMALL TEXT
================================= */

.small-text {
    color: #64748b;
    font-size: 13px;
}

/* =================================
   PRODUCT CARD DESIGN
================================= */

.product-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. PRODUCT DATABASE
# =====================================================

products = {
    "laptop": {
        "name": "Laptop",
        "price": 50000,
        "category": "Electronics",
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600",
        "description": "Powerful laptop for study and work."
    },

    "mouse": {
        "name": "Mouse",
        "price": 500,
        "category": "Accessories",
        "image": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=600",
        "description": "Comfortable and responsive computer mouse."
    },

    "keyboard": {
        "name": "Keyboard",
        "price": 1200,
        "category": "Accessories",
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600",
        "description": "Modern keyboard for everyday typing."
    },

    "headphones": {
        "name": "Headphones",
        "price": 2000,
        "category": "Audio",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600",
        "description": "Enjoy clear and immersive audio."
    },

    "pen": {
        "name": "Pen",
        "price": 10,
        "category": "Stationery",
        "image": "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=600",
        "description": "Smooth writing pen for everyday use."
    },

    "smartphone": {
        "name": "Smartphone",
        "price": 25000,
        "category": "Electronics",
        "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600",
        "description": "Feature-rich smartphone for communication and entertainment."
    },

    "tablet": {
        "name": "Tablet",
        "price": 18000,
        "category": "Electronics",
        "image": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600",
        "description": "Portable tablet for reading, learning and browsing."
    },

    "monitor": {
        "name": "Monitor",
        "price": 12000,
        "category": "Electronics",
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600",
        "description": "Clear display monitor for work and entertainment."
    },

    "printer": {
        "name": "Printer",
        "price": 8000,
        "category": "Electronics",
        "image": "https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=600",
        "description": "Convenient printer for home and office documents."
    },

    "usb drive": {
        "name": "USB Drive",
        "price": 600,
        "category": "Accessories",
        "image": "https://images.unsplash.com/photo-1623126908029-58cb08a2b272?w=600",
        "description": "Compact USB drive for storing and transferring files."
    },

    "bluetooth speaker": {
        "name": "Bluetooth Speaker",
        "price": 1500,
        "category": "Audio",
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600",
        "description": "Portable speaker with clear and powerful sound."
    },

    "earbuds": {
        "name": "Wireless Earbuds",
        "price": 2500,
        "category": "Audio",
        "image": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=600",
        "description": "Wireless earbuds for music and calls."
    },

    "microphone": {
        "name": "Microphone",
        "price": 1800,
        "category": "Audio",
        "image": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=600",
        "description": "Microphone for recording and online meetings."
    },

    "notebook": {
        "name": "Notebook",
        "price": 80,
        "category": "Stationery",
        "image": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=600",
        "description": "Notebook for notes and everyday writing."
    },

    "marker": {
        "name": "Marker Set",
        "price": 150,
        "category": "Stationery",
        "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=600",
        "description": "Colourful markers for writing and creative work."
    }
}

TAX_RATE = 0.18

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
        "description": "Get 15% OFF on purchases above ₹1,000"
    },

    "FESTIVE25": {
        "discount": 25,
        "min_purchase": 5000,
        "max_discount": 3000,
        "description": "Get 25% OFF on purchases above ₹5,000"
    }
}

categories = [
    "All",
    "Electronics",
    "Accessories",
    "Audio",
    "Stationery"
]

# =====================================================
# 4. SESSION STATE
# =====================================================

defaults = {
    "cart": {},
    "discount": 0,
    "coupon": "",
    "orders": [],
    "page": "Home",
    "search": "",
    "category": "All"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =====================================================
# 5. HELPER FUNCTIONS
# =====================================================

def money(amount):
    return f"₹{amount:,.2f}"


def product_label(name, qty):
    if name == "mouse":
        return "mouse" if qty == 1 else "mice"

    if name == "headphones":
        return "headphones"

    return products[name]["name"] if qty == 1 else products[name]["name"] + "s"


def add_to_cart(name):

    if name in st.session_state.cart:
        st.session_state.cart[name] += 1
    else:
        st.session_state.cart[name] = 1


def change_quantity(name, amount):

    new_qty = st.session_state.cart[name] + amount

    if new_qty <= 0:
        del st.session_state.cart[name]
    else:
        st.session_state.cart[name] = new_qty

    if not st.session_state.cart:
        st.session_state.discount = 0
        st.session_state.coupon = ""


def remove_from_cart(name):

    if name in st.session_state.cart:
        del st.session_state.cart[name]

    if not st.session_state.cart:
        st.session_state.discount = 0
        st.session_state.coupon = ""


def clear_cart():

    st.session_state.cart = {}
    st.session_state.discount = 0
    st.session_state.coupon = ""


def calculate_bill():

    subtotal = sum(
        products[name]["price"] * qty
        for name, qty in st.session_state.cart.items()
    )

    discount_amount = 0

    if st.session_state.coupon:
        coupon = coupons[st.session_state.coupon]

        discount_amount = min(
            subtotal * coupon["discount"] / 100,
            coupon["max_discount"]
        )

    taxable_amount = subtotal - discount_amount

    tax = taxable_amount * TAX_RATE

    grand_total = taxable_amount + tax

    return subtotal, discount_amount, tax, grand_total


#Dialogue box for order confirmation
@st.dialog("Confirm Your Order")
def confirm_order_dialog(order):

    st.write("Are you sure you want to place this order?")

    st.write("Grand Total:", money(order["total"]))

    if st.button("Confirm Order", type="primary"):

        st.session_state.orders.insert(0, order)

        clear_cart()

        st.session_state.last_order = order["order_id"]

        go_to("Orders")

        st.rerun()

    if st.button("Cancel"):
        st.rerun()

def total_cart_items():

    return sum(st.session_state.cart.values())


def go_to(page):

    st.session_state.page = page


# =====================================================
# 6. SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    logo_path = Path(__file__).parent / "ShopSmart.png"

with st.sidebar:
    st.image(str(logo_path), use_container_width=True)
    st.caption("Your everyday shopping destination")
    st.divider()


    menu = {
        "Home": "🏠 Home",
        "Cart": "🛒 My Cart",
        "Checkout": "💳 Checkout",
        "Orders": "📦 Order History"
    }

    for page, label in menu.items():

        if st.button(
            label,
            key=f"nav_{page}",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.page == page
                else "secondary"
            )
        ):

            st.session_state.page = page
            st.rerun()

    st.divider()

    st.metric(
        "Items in Cart",
        total_cart_items()
    )

    st.caption("Secure shopping demonstration")

    st.divider()

    st.caption("© 2026 ShopSmart")


# =====================================================
# 7. TOP HEADER
# =====================================================

header_col1, header_col2 = st.columns([4, 1])

with header_col1:

    st.markdown(
        f"<h2 style='color:#172554;'>"
        f"Welcome to ShopSmart 👋</h2>",
        unsafe_allow_html=True
    )

with header_col2:

    st.metric(
        "🛒 Cart Items",
        total_cart_items()
    )

st.divider()


# =====================================================
# 8. HOME PAGE
# =====================================================

if st.session_state.page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>Discover Your Favourite Products</h1>
        <p>
        Shop smart, save more and enjoy a better
        shopping experience.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Search bar

    st.subheader("🔍 Find Your Products")

    search_query = st.text_input(
        "Search products",
        placeholder="Search laptop, mouse, keyboard...",
        key="home_search"
    ).lower().strip()

    # Category filter

    selected_category = st.selectbox(
        "Choose Product Category",
        categories,
        key="home_category"
    )

    st.divider()

    st.subheader("🛍️ Explore Products")

    # Filter products

    filtered_products = []

    for key, product in products.items():

        matches_search = (
            search_query in product["name"].lower()
            or search_query in product["description"].lower()
            or search_query in product["category"].lower()
        )

        matches_category = (
            selected_category == "All"
            or product["category"] == selected_category
        )

        if matches_search and matches_category:
            filtered_products.append((key, product))

    if not filtered_products:

        st.warning("No products found. Try another search.")

    else:

        # Three products per row

        for start in range(0, len(filtered_products), 3):

            cols = st.columns(3)

            for col, (key, product) in zip(
                cols,
                filtered_products[start:start + 3]
            ):

                with col:

                    with st.container(
                        border=True,
                        key=f"product_card_{key}"
                    ):

                        st.markdown(
                            f"""
                            <div style="
                                width:100%;
                                height:180px;
                                overflow:hidden;
                                border-radius:10px;
                                margin-bottom:12px;
                            ">
                                <img src="{product['image']}"
                                    style="
                                        width:100%;
                                        height:180px;
                                        object-fit:cover;
                                        object-position:center;
                                    ">
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"### {product['name']}"
                        )

                        st.caption(product["category"])

                        st.write(product["description"])

                        st.markdown(
                            f"<div class='product-price'>"
                            f"{money(product['price'])}</div>",
                            unsafe_allow_html=True
                        )

                        if st.button(
                            "➕ Add to Cart",
                            key=f"add_{key}",
                            use_container_width=True
                        ):

                            add_to_cart(key)

                            st.toast(
                                f"{product['name']} added to cart!"
                            )

                            st.rerun()

    st.divider()

    if st.button(
        "🛒 View My Cart",
        type="primary"
    ):
        go_to("Cart")
        st.rerun()


# =====================================================
# 9. CART PAGE
# =====================================================

elif st.session_state.page == "Cart":

    st.title("🛒 My Shopping Cart")

    if not st.session_state.cart:

        st.info("Your shopping cart is empty.")

        if st.button("Continue Shopping", type="primary"):
            go_to("Home")
            st.rerun()

    else:

        st.write(
            f"You have {total_cart_items()} items in your cart."
        )

        st.divider()

        # Display cart products

        for name, qty in list(st.session_state.cart.items()):

            product = products[name]

            col1, col2, col3 = st.columns([1, 2, 2])

            with col1:

                st.image(
                    product["image"],
                    use_container_width=True
                )

            with col2:

                st.subheader(
                    product_label(name, qty).title()
                )

                st.caption(
                    f"Price per item: {money(product['price'])}"
                )

                st.write(
                    f"**Amount: {money(product['price'] * qty)}**"
                )

            with col3:

                st.write("Quantity")

                minus, quantity_col, plus = st.columns([1, 1, 1])

                with minus:

                    if st.button(
                        "➖",
                        key=f"minus_{name}"
                    ):
                        change_quantity(name, -1)
                        st.rerun()

                with quantity_col:

                    st.markdown(
                        f"<p style='text-align:center;"
                        f"font-size:20px;'>{qty}</p>",
                        unsafe_allow_html=True
                    )

                with plus:

                    if st.button(
                        "➕",
                        key=f"plus_{name}"
                    ):
                        change_quantity(name, 1)
                        st.rerun()

                if st.button(
                    "🗑️ Remove",
                    key=f"remove_{name}"
                ):
                    remove_from_cart(name)
                    st.rerun()

            st.divider()

        # Coupon section

        st.subheader("🎟️ Apply Coupon")

        # Calculate current cart subtotal
        subtotal = sum(
            products[name]["price"] * qty
            for name, qty in st.session_state.cart.items()
        )

        # Display available coupons
        with st.expander("🎁 View Available Coupons"):

            for code, details in coupons.items():

                st.markdown(f"**{code}**")

                st.caption(details["description"])

                st.write(
                    f"Maximum discount: {money(details['max_discount'])}"
                )

                st.divider()


        # Coupon input form
        with st.form("coupon_form"):

            coupon_code = st.text_input(
                "Enter Coupon Code",
                placeholder="e.g. SAVE10"
            ).upper().strip()

            apply_button = st.form_submit_button(
                "🎟️ Apply Coupon",
                use_container_width=True
            )

            if apply_button:

                if not coupon_code:

                    st.warning("Please enter a coupon code.")

                elif coupon_code not in coupons:

                    st.error("Invalid coupon code. Please try again.")

                elif subtotal < coupons[coupon_code]["min_purchase"]:

                    st.error(
                        f"This coupon requires a minimum purchase of "
                        f"{money(coupons[coupon_code]['min_purchase'])}."
                    )

                else:

                    st.session_state.coupon = coupon_code

                    st.success(
                        f"Congratulations! {coupon_code} applied successfully."
                    )


        # Display active coupon
        if st.session_state.coupon:

            active_coupon = coupons[st.session_state.coupon]

            st.success(
                f"Active Coupon: {st.session_state.coupon} "
                f"({active_coupon['discount']}% OFF)"
            )

            if st.button("❌ Remove Coupon"):

                st.session_state.coupon = ""
                st.session_state.discount = 0

                st.rerun()


        # Bill Summary
        st.divider()

        st.subheader("🧾 Cart Summary")

        subtotal, discount, tax, total = calculate_bill()

        st.write("Subtotal:", money(subtotal))
        st.write("Discount:", money(discount))
        st.write("GST (18%):", money(tax))

        st.markdown("---")

        st.markdown(
            f"<h2 style='color:#2563eb;'>"
            f"Grand Total: {money(total)}</h2>",
            unsafe_allow_html=True
        )

        # Navigation Buttons
        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Continue Shopping",
                use_container_width=True
            ):
                go_to("Home")
                st.rerun()

        with col2:

            if st.button(
                "Proceed to Checkout ➜",
                type="primary",
                use_container_width=True
            ):
                go_to("Checkout")
                st.rerun()


# =====================================================
# 10. CHECKOUT PAGE
# =====================================================

elif st.session_state.page == "Checkout":

    st.title("💳 Checkout")

    if not st.session_state.cart:

        st.warning("Your cart is empty. Add products before checkout.")

        if st.button("Go Shopping"):
            go_to("Home")
            st.rerun()

    else:

        st.subheader("Order Details")

        subtotal, discount, tax, total = calculate_bill()

        # Order overview

        with st.container(border=True):

            for name, qty in st.session_state.cart.items():

                st.write(
                    f"**{product_label(name, qty).title()}** "
                    f"× {qty} — "
                    f"{money(products[name]['price'] * qty)}"
                )

            st.divider()

            st.write("Subtotal:", money(subtotal))

            st.write("Discount:", money(discount))

            st.write("GST (18%):", money(tax))

            st.markdown(f"### Total: {money(total)}")

        st.divider()

        st.subheader("Customer Information")

        with st.form("checkout_form"):

            customer_name = st.text_input(
                "Full Name"
            )

            email = st.text_input(
                "Email Address"
            )

            phone = st.text_input(
                "Phone Number"
            )

            address = st.text_area(
                "Delivery Address"
            )

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Cash on Delivery",
                    "UPI (Demo)",
                    "Card (Demo)"
                ]
            )

            place_order = st.form_submit_button(
                "Place Order",
                type="primary",
                use_container_width=True
            )

            if place_order:

                if not all([
                    customer_name.strip(),
                    email.strip(),
                    phone.strip(),
                    address.strip()
                ]):

                    st.error(
                        "Please fill in all customer details."
                    )

                elif "@" not in email or "." not in email.split("@")[-1]:

                    st.error("Please enter a valid email address.")

                elif not phone.isdigit() or len(phone) != 10:

                    st.error(
                        "Enter a valid 10-digit phone number."
                    )

                else:

                    # Save order before clearing cart

                    order = {
                        "order_id": str(uuid.uuid4())[:8].upper(),
                        "date": datetime.now().strftime(
                            "%d-%m-%Y %I:%M %p"
                        ),
                        "customer": customer_name,
                        "email": email,
                        "phone": phone,
                        "address": address,
                        "payment": payment_method,
                        "items": [
                            {
                                "name": name,
                                "qty": qty,
                                "price": products[name]["price"]
                            }
                            for name, qty
                            in st.session_state.cart.items()
                        ],
                        "subtotal": subtotal,
                        "discount": discount,
                        "tax": tax,
                        "total": total,
                        "coupon": st.session_state.coupon,
                        "status": "Order Placed"
                    }

                    confirm_order_dialog(order)


# =====================================================
# 11. ORDER HISTORY PAGE
# =====================================================

elif st.session_state.page == "Orders":

    st.title("📦 Order History")

    st.write("View all your previously placed orders.")

    if not st.session_state.orders:

        st.info(
            "You haven't placed any orders yet."
        )

        if st.button("Start Shopping", type="primary"):

            go_to("Home")
            st.rerun()

    else:

        st.metric(
            "Total Orders",
            len(st.session_state.orders)
        )

        st.divider()

        for order in st.session_state.orders:

            with st.expander(
                f"Order #{order['order_id']} | "
                f"{order['date']} | "
                f"{money(order['total'])}"
            ):

                st.write(
                    "**Customer:**",
                    order["customer"]
                )

                st.write(
                    "**Email:**",
                    order["email"]
                )

                st.write(
                    "**Delivery Address:**",
                    order["address"]
                )

                st.write(
                    "**Payment Method:**",
                    order["payment"]
                )

                st.write(
                    "**Status:**",
                    order["status"]
                )

                st.divider()

                st.write("### Ordered Products")

                for item in order["items"]:

                    st.write(
                        f"- {product_label(item['name'], item['qty']).title()} "
                        f"× {item['qty']} = "
                        f"{money(item['price'] * item['qty'])}"
                    )

                st.divider()

                st.write(
                    "Subtotal:",
                    money(order["subtotal"])
                )

                st.write(
                    "Discount:",
                    money(order["discount"])
                )

                st.write(
                    "GST:",
                    money(order["tax"])
                )

                st.markdown(
                    f"### Total: {money(order['total'])}"
                )

                st.caption(
                    f"Coupon: {order['coupon'] or 'Not applied'}"
                )


# =====================================================
# 12. FOOTER
# =====================================================



st.divider()

logo_path = Path(__file__).parent / "ShopSmart.png"

with open(logo_path, "rb") as image_file:
    logo_base64 = base64.b64encode(image_file.read()).decode()

st.markdown(f"""
<div style="width:100%; text-align:center; padding:20px 0;">
<img src="data:image/png;base64,{logo_base64}"
style="display:block; width:180px; height:auto; margin:0 auto 12px auto;">

<p style="color:#64748b; font-size:14px; margin:4px 0; font-weight:500;">
Your everyday shopping destination.
</p>

<p style="color:#94a3b8; font-size:12px; margin:5px 0;">
© 2026 ShopSmart. All Rights Reserved.
</p>

<small style="color:#94a3b8; font-size:11px;">
Developed with Python &amp; Streamlit
</small>
</div>
""", unsafe_allow_html=True)
