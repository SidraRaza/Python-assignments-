import streamlit as st 

# Custom CSS for Styling
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #1f1c2c, #928DAB);
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        background: #222;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 0px 20px rgba(255, 255, 255, 0.1);
    }
    h1 {
        text-align: center;
        font-size: 42px;
        color: #00c9ff;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .stButton>button {
        background: #00c9ff;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        font-size: 18px;
        box-shadow: 0px 5px 15px rgba(0, 201, 255, 0.4);
        transition: 0.3s;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: #ff8c00;
        transform: scale(1.05);
    }
    .result-box {
        font-size: 22px;
        font-weight: bold;
        text-align: center;
        background: rgba(255, 255, 255, 0.15);
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
        box-shadow: 0px 5px 20px rgba(0,201,255,0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        font-size: 14px;
        color: white !important;
        opacity: 1 !important;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title & Description
st.markdown("<h1>Unit Converter</h1>", unsafe_allow_html=True)
st.write("Easily convert between units of measurement with a modern design.")

# Sidebar menu for conversion selection
conversion_type = st.sidebar.selectbox("Choose Conversion Type", ["Length", "Weight", "Temperature"])
value = st.number_input("Enter Value", value=0.0, min_value=0.0, step=0.1)
col1, col2 = st.columns(2)

# Conversion Logic
conversion_factors = {
    # Length
    "Meters-Kilometers": 0.001, "Kilometers-Meters": 1000, "Meters-Millimeters": 1000, "Millimeters-Meters": 0.001,
    "Meters-Miles": 0.000621371, "Miles-Meters": 1609.34, "Meters-Yards": 1.09361, "Yards-Meters": 0.9144,
    "Meters-Centimeters": 100, "Centimeters-Meters": 0.01, "Meters-Feet": 3.28084, "Feet-Meters": 0.3048,
    "Meters-Inches": 39.3701, "Inches-Meters": 0.0254,

    # Weight
    "Kilograms-Grams": 1000, "Grams-Kilograms": 0.001, "Kilograms-Milligrams": 1000000, "Milligrams-Kilograms": 0.000001,
    "Kilograms-Pounds": 2.20462, "Pounds-Kilograms": 0.453592, "Kilograms-Ounces": 35.274, "Ounces-Kilograms": 0.0283495
}

# Input Fields
if conversion_type in ["Length", "Weight"]:
    with col1:
        from_unit = st.selectbox("From", list(set([k.split("-")[0] for k in conversion_factors.keys() if k.startswith(conversion_type[0])])))
    with col2:
        to_unit = st.selectbox("To", list(set([k.split("-")[1] for k in conversion_factors.keys() if k.startswith(conversion_type[0])])))
    
    key = f"{from_unit}-{to_unit}"
    result = value * conversion_factors.get(key, 1)

elif conversion_type == "Temperature":
    with col1:
        from_unit = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"])
    with col2:
        to_unit = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"])
    
    if from_unit == "Celsius" and to_unit == "Fahrenheit":
        result = (value * 1.8) + 32
    elif from_unit == "Fahrenheit" and to_unit == "Celsius":    
        result = (value - 32) / 1.8
    elif from_unit == "Celsius" and to_unit == "Kelvin":
        result = value + 273.15
    elif from_unit == "Kelvin" and to_unit == "Celsius":
        result = value - 273.15
    elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
        result = (value - 32) / 1.8 + 273.15
    elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
        result = (value - 273.15) * 1.8 + 32
    else:
        result = value

# Display Result
st.markdown(f"<div class='result-box'>{value} {from_unit} is equal to {result:.2f} {to_unit}</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class='footer'>
        Developed with ❤️ by <a href='https://github.com/SidraRaza' target='_blank' style='color: white; text-decoration: none;'>Sidra Raza</a> using Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
