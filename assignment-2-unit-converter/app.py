import streamlit as st

def convert_length(value, from_unit, to_unit):
    conversion_factors = {
        "Meters-Kilometers": 0.001, "Kilometers-Meters": 1000,
        "Meters-Millimeters": 1000, "Millimeters-Meters": 0.001,
        "Meters-Miles": 0.000621371, "Miles-Meters": 1609.34,
        "Meters-Yards": 1.09361, "Yards-Meters": 0.9144,
        "Meters-Centimeters": 100, "Centimeters-Meters": 0.01,
        "Meters-Feet": 3.28084, "Feet-Meters": 0.3048,
        "Meters-Inches": 39.3701, "Inches-Meters": 0.0254,
        "Feet-Inches": 12, "Inches-Feet": 1/12,
        "Yards-Feet": 3, "Feet-Yards": 1/3
    }
    return value * conversion_factors.get(f"{from_unit}-{to_unit}", 1)

def convert_weight(value, from_unit, to_unit):
    conversion_factors = {
        "Kilograms-Grams": 1000, "Grams-Kilograms": 0.001,
        "Kilograms-Milligrams": 1000000, "Milligrams-Kilograms": 0.000001,
        "Kilograms-Pounds": 2.20462, "Pounds-Kilograms": 0.453592,
        "Kilograms-Ounces": 35.274, "Ounces-Kilograms": 0.0283495,
        "Grams-Milligrams": 1000, "Milligrams-Grams": 0.001,
        "Pounds-Ounces": 16, "Ounces-Pounds": 1/16
    }
    return value * conversion_factors.get(f"{from_unit}-{to_unit}", 1)

def convert_temperature(value, from_unit, to_unit):
    if from_unit == "Celsius" and to_unit == "Fahrenheit":
        return (value * 1.8) + 32
    elif from_unit == "Fahrenheit" and to_unit == "Celsius":
        return (value - 32) / 1.8
    elif from_unit == "Celsius" and to_unit == "Kelvin":
        return value + 273.15
    elif from_unit == "Kelvin" and to_unit == "Celsius":
        return value - 273.15
    elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
        return (value - 32) / 1.8 + 273.15
    elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
        return (value - 273.15) * 1.8 + 32
    return value

st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1f1c2c, #928DAB);
        color: white;
        font-family: 'Arial', sans-serif;
    }
    h1 {
        text-align: center;
        color: #00c9ff;
    }
    .result-box {
        text-align: center;
        background: rgba(255, 255, 255, 0.15);
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        font-size: 14px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>Unit Converter</h1>", unsafe_allow_html=True)
st.write("Easily convert between different units of measurement with a modern UI.")

conversion_type = st.sidebar.selectbox("Choose Conversion Type", ["Length", "Weight", "Temperature"])
value = st.number_input("Enter Value", value=0.0, min_value=0.0, step=0.1)
col1, col2 = st.columns(2)

if conversion_type == "Length":
    with col1:
        from_unit = st.selectbox("From", ["Meters", "Kilometers", "Millimeters", "Miles", "Yards", "Centimeters", "Feet", "Inches"])
    with col2:
        to_unit = st.selectbox("To", ["Meters", "Kilometers", "Millimeters", "Miles", "Yards", "Centimeters", "Feet", "Inches"])
    result = convert_length(value, from_unit, to_unit)

elif conversion_type == "Weight":
    with col1:
        from_unit = st.selectbox("From", ["Kilograms", "Grams", "Milligrams", "Pounds", "Ounces"])
    with col2:
        to_unit = st.selectbox("To", ["Kilograms", "Grams", "Milligrams", "Pounds", "Ounces"])
    result = convert_weight(value, from_unit, to_unit)

elif conversion_type == "Temperature":
    with col1:
        from_unit = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"])
    with col2:
        to_unit = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"])
    result = convert_temperature(value, from_unit, to_unit)

st.markdown(f"<div class='result-box'>{value} {from_unit} is equal to {result:.2f} {to_unit}</div>", unsafe_allow_html=True)
st.markdown("<div class='footer'>Developed with ❤️ by <a href='https://github.com/SidraRaza' target='_blank' style='color: white;'>Sidra Raza</a></div>", unsafe_allow_html=True)