import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="OrderShield AI",
    page_icon="🛡️",
    layout="wide"
)

# ----------------------------
# LOAD MODELS
# ----------------------------
model = joblib.load("models/risk_model.pkl")
encoder = joblib.load("models/encoder.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

# ----------------------------
# CUSTOM CSS
# ----------------------------
st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.title {
    font-size: 50px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg,#00ffe1,#4facfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub {
    text-align:center;
    color:#bdbdbd;
    font-size:18px;
    margin-bottom:25px;
}

.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.markdown(
    "<div class='title'>🇵🇰 PakShield AI</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub'>Pakistan E-Commerce Risk Intelligence Platform</div>",
    unsafe_allow_html=True
)

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.header("📦 Order Information")

country = st.sidebar.selectbox(
    "Country",
    ['Belgium','Netherlands','Italy','Germany','Turkey','France','Spain','Poland']
)

device_type = st.sidebar.selectbox(
    "Device Type",
    ['Mobile','Desktop','Tablet']
)

traffic_source = st.sidebar.selectbox(
    "Traffic Source",
    ['Paid Ads','Email','Organic Search','Direct','Social Media','Marketplace']
)

payment_method = st.sidebar.selectbox(
    "Payment Method",
    ['Credit Card','Debit Card','Klarna','Bank Transfer','PayPal','Gift Card']
)

product_category = st.sidebar.selectbox(
    "Product Category",
    ['Sports','Garden','Electronics','Home & Kitchen','Pet Supplies','Beauty','Toys','Fashion']
)

customer_age_days = st.sidebar.number_input(
    "Customer Age (Days)",
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

avg_order_value = st.sidebar.number_input(
    "Average Order Value (€)",
    min_value=0.0,
    max_value=100000.0,
    value=100.0
)

order_value = st.sidebar.number_input(
    "Current Order Value (€)",
    min_value=0.0,
    max_value=100000.0,
    value=120.0
)

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
    max_value=50000,
    value=500
)

delivery_days = st.sidebar.number_input(
    "Estimated Delivery Days",
    min_value=1,
    max_value=30,
    value=5
)

late_delivery_risk = st.sidebar.selectbox(
    "Late Delivery Risk",
    [0, 1]
)

address_mismatch = st.sidebar.selectbox(
    "Address Mismatch",
    [0, 1]
)

high_risk_ip = st.sidebar.selectbox(
    "High Risk IP",
    [0, 1]
)

# ----------------------------
# FEATURE ENGINEERING
# ----------------------------
order_value_per_item = order_value / max(quantity, 1)

customer_value_ratio = order_value / (avg_order_value + 1)

discount_amount = order_value * discount_rate

# ----------------------------
# PREDICT BUTTON
# ----------------------------
if st.button("🔍 Analyze Order Risk", use_container_width=True):

    data = pd.DataFrame([{
        "country": country,
        "device_type": device_type,
        "traffic_source": traffic_source,
        "payment_method": payment_method,
        "product_category": product_category,
        "customer_age_days": customer_age_days,
        "previous_orders": previous_orders,
        "avg_order_value_eur": avg_order_value,
        "order_value_eur": order_value,
        "quantity": quantity,
        "discount_rate": discount_rate,
        "shipping_distance_km": shipping_distance,
        "delivery_days_estimated": delivery_days,
        "late_delivery_risk": late_delivery_risk,
        "address_mismatch": address_mismatch,
        "high_risk_ip": high_risk_ip,
        "order_value_per_item": order_value_per_item,
        "customer_value_ratio": customer_value_ratio,
        "discount_amount": discount_amount
    }])

    # ----------------------------
    # ENCODE CATEGORICAL
    # ----------------------------
    cat_cols = [
        "country",
        "device_type",
        "traffic_source",
        "payment_method",
        "product_category"
    ]

    data[cat_cols] = encoder.transform(data[cat_cols])

    # ----------------------------
    # EXACT TRAINING FEATURE ORDER
    # ----------------------------
    data = data[[
        'country',
        'device_type',
        'traffic_source',
        'payment_method',
        'product_category',
        'customer_age_days',
        'previous_orders',
        'avg_order_value_eur',
        'order_value_eur',
        'quantity',
        'discount_rate',
        'shipping_distance_km',
        'delivery_days_estimated',
        'late_delivery_risk',
        'address_mismatch',
        'high_risk_ip',
        'order_value_per_item',
        'customer_value_ratio',
        'discount_amount'
    ]]

    # ----------------------------
    # PREDICTION
    # ----------------------------
    pred = model.predict(data)[0]
    proba = model.predict_proba(data)[0]

    confidence = np.max(proba) * 100

    label = label_encoder.inverse_transform([pred])[0]

    # ----------------------------
    # DASHBOARD
    # ----------------------------
    col1, col2, col3 = st.columns(3)

    risk_score = confidence

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        title={"text": "Risk Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "steps": [
                {"range": [0, 40], "color": "green"},
                {"range": [40, 70], "color": "orange"},
                {"range": [70, 100], "color": "red"}
            ]
        }
    ))

    col1.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("Prediction")

        if label == "Fraud Risk":
            st.error("🚨 Fraud Risk")

        elif label == "Return Risk":
            st.warning("⚠️ Return Risk")

        else:
            st.success("✅ Normal")

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

    with col3:

        prob_df = pd.DataFrame({
            "Class": label_encoder.classes_,
            "Probability": proba
        })

        fig2 = px.bar(
            prob_df,
            x="Class",
            y="Probability",
            color="Class"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.divider()

    st.subheader("🧠 Business Decision")

    if label == "Fraud Risk":
        st.error("BLOCK ORDER - Potential fraud detected")

    elif label == "Return Risk":
        st.warning("HOLD FOR REVIEW - Possible return abuse")

    else:
        st.success("APPROVE ORDER - Safe transaction")

    st.divider()

    st.subheader("🔍 Risk Signals")

    reasons = []

    if high_risk_ip == 1:
        reasons.append("High-risk IP detected")

    if address_mismatch == 1:
        reasons.append("Address mismatch detected")

    if discount_rate > 0.40:
        reasons.append("Unusually high discount")

    if previous_orders == 0:
        reasons.append("New customer account")

    if order_value > avg_order_value * 3:
        reasons.append("Order value anomaly")

    if reasons:
        for reason in reasons:
            st.write(f"• {reason}")
    else:
        st.success("No major risk indicators detected")

# ----------------------------
# FOOTER
# ----------------------------
st.divider()
st.caption(
    "PakShield AI • Pakistan E-Commerce Risk Intelligence System"
)
