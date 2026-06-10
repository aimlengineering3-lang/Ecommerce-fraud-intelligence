# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.header("📦 Order Information")

# ============================
# PROVINCE MAPPING
# ============================

province_map = {
    "Punjab": "Germany",
    "Sindh": "France",
    "Khyber Pakhtunkhwa (KPK)": "Spain",
    "Balochistan": "Italy",
    "Islamabad Capital Territory": "Belgium",
    "Azad Kashmir (AJK)": "Netherlands",
    "Gilgit Baltistan": "Poland",
    "Overseas Pakistani": "Turkey"
}

selected_province = st.sidebar.selectbox(
    "Province",
    list(province_map.keys())
)

country = province_map[selected_province]

# ============================
# DEVICE TYPE
# ============================

device_type = st.sidebar.selectbox(
    "Device Type",
    ["Mobile", "Desktop", "Tablet"]
)

# ============================
# TRAFFIC SOURCE MAPPING
# ============================

traffic_map = {
    "Facebook Ads": "Paid Ads",
    "Instagram Ads": "Email",
    "Google Search": "Organic Search",
    "Direct Website Visit": "Direct",
    "TikTok Shop": "Social Media",
    "Daraz Marketplace": "Marketplace"
}

selected_traffic = st.sidebar.selectbox(
    "Traffic Source",
    list(traffic_map.keys())
)

traffic_source = traffic_map[selected_traffic]

# ============================
# PAYMENT METHOD MAPPING
# ============================

payment_map = {
    "Cash on Delivery (COD)": "Credit Card",
    "Easypaisa": "Debit Card",
    "JazzCash": "PayPal",
    "Bank Transfer": "Bank Transfer",
    "Credit Card": "Credit Card",
    "Debit Card": "Gift Card"
}

selected_payment = st.sidebar.selectbox(
    "Payment Method",
    list(payment_map.keys())
)

payment_method = payment_map[selected_payment]

# ============================
# PRODUCT CATEGORY
# ============================

product_category = st.sidebar.selectbox(
    "Product Category",
    [
        "Electronics",
        "Fashion",
        "Beauty",
        "Home & Kitchen",
        "Sports",
        "Pet Supplies",
        "Toys",
        "Garden"
    ]
)

# ============================
# CUSTOMER PROFILE
# ============================

customer_age_days = st.sidebar.number_input(
    "Account Age (Days)",
    min_value=0,
    max_value=5000,
    value=100
)

previous_orders = st.sidebar.number_input(
    "Previous Orders",
    min_value=0,
    max_value=500,
    value=2
)

# ============================
# PKR VALUES
# ============================

avg_order_value_pkr = st.sidebar.number_input(
    "Average Order Value (PKR)",
    min_value=100.0,
    max_value=5000000.0,
    value=5000.0
)

order_value_pkr = st.sidebar.number_input(
    "Current Order Value (PKR)",
    min_value=100.0,
    max_value=5000000.0,
    value=8000.0
)

# Convert PKR to EUR equivalent
avg_order_value = avg_order_value_pkr / 320
order_value = order_value_pkr / 320

# ============================
# ORDER DETAILS
# ============================

quantity = st.sidebar.number_input(
    "Quantity",
    min_value=1,
    max_value=100,
    value=1
)

discount_rate = st.sidebar.slider(
    "Discount Rate",
    0.0,
    1.0,
    0.10
)

shipping_distance = st.sidebar.number_input(
    "Shipping Distance (KM)",
    min_value=0,
    max_value=5000,
    value=150
)

delivery_days = st.sidebar.number_input(
    "Estimated Delivery Days",
    min_value=1,
    max_value=30,
    value=5
)

# ============================
# ADVANCED RISK SIGNALS
# ============================

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛡️ Merchant Verification")

late_delivery_risk = st.sidebar.selectbox(
    "Late Delivery Risk",
    [0, 1],
    help="0 = No, 1 = Yes"
)

address_mismatch = st.sidebar.selectbox(
    "Address Mismatch",
    [0, 1],
    help="0 = No, 1 = Yes"
)

high_risk_ip = st.sidebar.selectbox(
    "High Risk IP",
    [0, 1],
    help="0 = Safe, 1 = Suspicious"
)
