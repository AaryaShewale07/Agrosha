import numpy as np
import pandas as pd
import os
from flask import Flask, request, render_template_string, send_from_directory, send_file
import io
from xhtml2pdf import pisa

# Create a simple Flask app
app = Flask(__name__)

# Define the HTML template as a string directly in the code
# This eliminates any issues with template directories
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">c
<head>
  <meta charset="UTF-8">
  <title>Crop Yield Prediction</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      padding: 20px;
      background-color: #f9f9f9;
    }
    
    .form-container {
      max-width: 800px;
      margin: 0 auto;
      background-color: white;
      padding: 25px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    h2 {
      color: #33691E;
      text-align: center;
      margin-bottom: 25px;
    }
    
    .form-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
    }
    
    .form-group {
      flex: 1 1 45%;
      display: flex;
      flex-direction: column;
      margin-bottom: 15px;
    }
    
    .full-width {
      flex: 1 1 100%;
    }
    
    label {
      margin-bottom: 6px;
      font-weight: 500;
      color: #555;
    }
    
    select, input {
      padding: 10px;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 16px;
    }
    
    button {
      background-color: #33691E;
      color: white;
      border: none;
      padding: 12px;
      border-radius: 4px;
      font-size: 16px;
      cursor: pointer;
      transition: background-color 0.3s;
      width: 100%;
    }
    
    button:hover {
      background-color: #558B2F;
    }
    
    .result-box {
      margin-top: 30px;
      padding: 20px;
      background-color: #f5f9f5;
      border-radius: 6px;
      border-left: 5px solid #33691E;
    }
    
    .result-box h3 {
      margin-top: 0;
      color: #333;
    }
    
    .result-box ul {
      list-style-type: none;
      padding: 0;
      margin: 15px 0 0 0;
    }
    
    .result-box ul li {
      padding: 8px 0;
      border-bottom: 1px solid #eee;
    }
    
    .result-box ul li:last-child {
      border-bottom: none;
    }
    
    .error-message {
      background-color: #ffebee;
      border-left: 5px solid #c62828;
      padding: 15px;
      margin-top: 20px;
      border-radius: 6px;
    }
  </style>
</head>
<body>
  <div class="form-container">
    <h2>Crop Yield Prediction</h2>
    
    {% if error %}
    <div class="error-message">
      {{ error }}
    </div>
    {% endif %}
    
    <form action="/predict" method="POST" class="form-grid">
      <div class="form-group">
        <label for="year">Crop Year</label>
        <select id="year" name="Crop_Year" required>
          <option disabled selected>Select Year</option>
          <script>
            for(let year = 1997; year <= 2020; year++) {
              document.write(`<option value="${year}">${year}</option>`);
            }
          </script>
        </select>
      </div>

      <div class="form-group">
        <label for="state">State</label>
        <select id="state" name="State" required>
          <option disabled selected>Select State</option>
          <option>Andhra Pradesh</option>
          <option>Arunachal Pradesh</option>
          <option>Assam</option>
          <option>Bihar</option>
          <option>Chhattisgarh</option>
          <option>Delhi</option>
          <option>Goa</option>
          <option>Gujarat</option>
          <option>Haryana</option>
          <option>Himachal Pradesh</option>
          <option>Jammu and Kashmir</option>
          <option>Jharkhand</option>
          <option>Karnataka</option>
          <option>Kerala</option>
          <option>Madhya Pradesh</option>
          <option>Maharashtra</option>
          <option>Manipur</option>
          <option>Meghalaya</option>
          <option>Mizoram</option>
          <option>Nagaland</option>
          <option>Odisha</option>
          <option>Puducherry</option>
          <option>Punjab</option>
          <option>Sikkim</option>
          <option>Tamil Nadu</option>
          <option>Telangana</option>
          <option>Tripura</option>
          <option>Uttar Pradesh</option>
          <option>Uttarakhand</option>
          <option>West Bengal</option>
        </select>
      </div>

      <div class="form-group">
        <label for="season">Season</label>
        <select id="season" name="Season" required>
          <option disabled selected>Select Season</option>
          <option>Summer</option>
          <option>Winter</option>
          <option>Monsoon</option>
          <option>Monsoon-Winter</option>
        </select>
      </div>

      <div class="form-group">
        <label for="crop">Crop</label>
        <select id="crop" name="Crop" required>
          <option disabled selected>Select Crop</option>
          <option>Arecanut</option>
          <option>Arhar/Tur</option>
          <option>Bajra</option>
          <option>Banana</option>
          <option>Barley</option>
          <option>Black pepper</option>
          <option>Cardamom</option>
          <option>Cashewnut</option>
          <option>Castor seed</option>
          <option>Coconut</option>
          <option>Coriander</option>
          <option>Cotton(lint)</option>
          <option>Cowpea(Lobia)</option>
          <option>Dry chillies</option>
          <option>Garlic</option>
          <option>Ginger</option>
          <option>Gram</option>
          <option>Groundnut</option>
          <option>Guar seed</option>
          <option>Horse-gram</option>
          <option>Jowar</option>
          <option>Jute</option>
          <option>Khesari</option>
          <option>Linseed</option>
          <option>Maize</option>
          <option>Masoor</option>
          <option>Mesta</option>
          <option>Moong (Green Gram)</option>
          <option>Moth</option>
          <option>Niger seed</option>
          <option>Oilseeds total</option>
          <option>Onion</option>
          <option>Other Rabi pulses</option>
          <option>Other Cereals</option>
          <option>Other Kharif pulses</option>
          <option>Other oilseeds</option>
          <option>Other Summer Pulses</option>
          <option>Peas & beans (Pulses)</option>
          <option>Potato</option>
          <option>Ragi</option>
          <option>Rapeseed & Mustard</option>
          <option>Rice</option>
          <option>Safflower</option>
          <option>Sannhamp</option>
          <option>Sesamum</option>
          <option>Small millets</option>
          <option>Soyabean</option>
          <option>Sugarcane</option>
          <option>Sunflower</option>
          <option>Sweet potato</option>
          <option>Tapioca</option>
          <option>Tobacco</option>
          <option>Turmeric</option>
          <option>Urad</option>
          <option>Wheat</option>
        </select>
      </div>

      <div class="form-group">
        <label for="area">Area (in hectares)</label>
        <input type="number" id="area" name="Area" placeholder="Enter area in hectares" step="0.01" min="0.1" required>
      </div>

      <div class="form-group full-width">
        <button type="submit">Predict Yield</button>
      </div>
    </form>

    {% if predicted_value %}
    <div class="result-box">
      <h3>Predicted Yield: <span style="color: #33691E;">{{ predicted_value }} tons/hectare</span></h3>
      <ul>
        <li><strong>Production:</strong> {{ production }} tons</li>
        <li><strong>Annual Rainfall:</strong> {{ rainfall }} mm</li>
        <li><strong>Fertilizer:</strong> {{ fertilizer }} kg/hectare</li>
        <li><strong>Pesticide:</strong> {{ pesticide }} kg/hectare</li>
        <li><strong>Price per Ton:</strong> ₹{{ price_per_ton }}</li>
        <li><strong>Investment:</strong> ₹{{ investment }}</li>
        <li><strong>Profit:</strong> ₹{{ profit }}</li>
      </ul>
    </div>
    {% endif %}
  </div>
</body>
</html>
"""

# Crop prices dictionary
CROP_PRICES = {
    'Arecanut': 20000,
    'Arhar/Tur': 46000,
    'Bajra': 20000,
    'Banana': 8000,
    'Barley': 19000,
    'Black pepper': 20000,
    'Cardamom': 20000,
    'Cashewnut': 20000,
    'Castor seed': 20000,
    'Coconut': 20000,
    'Coriander': 20000,
    'Cotton(lint)': 45000,
    'Cowpea(Lobia)': 20000,
    'Dry chillies': 20000,
    'Garlic': 60000,
    'Ginger': 55000,
    'Gram': 50000,
    'Groundnut': 42000,
    'Guar seed': 20000,
    'Horse-gram': 20000,
    'Jowar': 20000,
    'Jute': 35000,
    'Khesari': 20000,
    'Linseed': 20000,
    'Maize': 18000,
    'Masoor': 20000,
    'Mesta': 20000,
    'Moong (Green Gram)': 48000,
    'Moth': 20000,
    'Niger seed': 20000,
    'Oilseeds total': 20000,
    'Onion': 7000,
    'Other Rabi pulses': 20000,
    'Other Cereals': 20000,
    'Other Kharif pulses': 20000,
    'Other oilseeds': 20000,
    'Other Summer Pulses': 20000,
    'Peas & beans (Pulses)': 20000,
    'Potato': 6000,
    'Ragi': 20000,
    'Rapeseed & Mustard': 20000,
    'Rice': 21000,
    'Safflower': 20000,
    'Sannhamp': 20000,
    'Sesamum': 20000,
    'Small millets': 20000,
    'Soyabean': 40000,
    'Sugarcane': 3000,
    'Sunflower': 20000,
    'Sweet potato': 20000,
    'Tapioca': 20000,
    'Tobacco': 20000,
    'Turmeric': 90000,
    'Urad': 47000,
    'Wheat': 22000
}

# Dummy prediction function (since we don't have the actual models)
def predict_crop_yield(crop, year, state, season, area):
    # These are dummy values for demonstration
    base_yields = {
        'Arecanut': 2.8,
        'Arhar/Tur': 0.9,
        'Bajra': 1.2,
        'Banana': 22.0,
        'Barley': 2.5,
        'Black pepper': 0.5,
        'Cardamom': 0.3,
        'Cashewnut': 0.8,
        'Castor seed': 1.0,
        'Coconut': 10000.0, # nuts per hectare
        'Coriander': 0.8,
        'Cotton(lint)': 0.5,
        'Cowpea(Lobia)': 0.7,
        'Dry chillies': 1.5,
        'Garlic': 5.0,
        'Ginger': 4.0,
        'Gram': 1.0,
        'Groundnut': 1.2,
        'Guar seed': 0.8,
        'Horse-gram': 0.6,
        'Jowar': 1.0,
        'Jute': 2.5,
        'Khesari': 0.7,
        'Linseed': 0.6,
        'Maize': 3.0,
        'Masoor': 0.8,
        'Mesta': 1.5,
        'Moong (Green Gram)': 0.7,
        'Moth': 0.5,
        'Niger seed': 0.4,
        'Oilseeds total': 1.0,
        'Onion': 15.0,
        'Other Rabi pulses': 0.8,
        'Other Cereals': 1.2,
        'Other Kharif pulses': 0.8,
        'Other oilseeds': 0.9,
        'Other Summer Pulses': 0.7,
        'Peas & beans (Pulses)': 1.0,
        'Potato': 20.0,
        'Ragi': 1.5,
        'Rapeseed & Mustard': 1.1,
        'Rice': 2.8,
        'Safflower': 0.7,
        'Sannhamp': 1.0,
        'Sesamum': 0.4,
        'Small millets': 0.8,
        'Soyabean': 1.3,
        'Sugarcane': 70.0,
        'Sunflower': 0.8,
        'Sweet potato': 10.0,
        'Tapioca': 25.0,
        'Tobacco': 1.7,
        'Turmeric': 5.0,
        'Urad': 0.6,
        'Wheat': 3.2
    }
    
    rainfall_map = {
        'Summer': 800,
        'Winter': 200,
        'Monsoon': 1500,
        'Monsoon-Winter': 900
    }
    
    # Adjust yield based on state (simple multiplier)
    state_multipliers = {
        'Punjab': 1.2,
        'Uttar Pradesh': 1.05,
        'Maharashtra': 0.95,
        'Karnataka': 1.1,
        'Tamil Nadu': 1.08,
        'Andhra Pradesh': 1.03,
        'Gujarat': 0.97,
        'Haryana': 1.15,
        'Madhya Pradesh': 0.92,
        'West Bengal': 1.1,
        'Bihar': 0.9,
        'Rajasthan': 0.85,
        'Odisha': 0.93,
        'Kerala': 1.05,
        'Telangana': 1.0
    }
    
    # Default multiplier if state not in the dictionary
    state_multiplier = state_multipliers.get(state, 1.0)
    
    # Base values
    base_yield = base_yields.get(crop, 1.0)
    year_factor = min(1.2, max(0.8, (year - 1997) / 50 + 1))  # Slight increase over years
    
    # Calculate values
    predicted_yield = base_yield * state_multiplier * year_factor
    rainfall = rainfall_map.get(season, 800)
    
    # Fertilizer and pesticide recommendations based on crop type
    crop_categories = {
        'cereals': ['Rice', 'Wheat', 'Maize', 'Bajra', 'Jowar', 'Barley', 'Ragi', 'Small millets', 'Other Cereals'],
        'pulses': ['Arhar/Tur', 'Gram', 'Moong (Green Gram)', 'Urad', 'Masoor', 'Other Kharif pulses', 'Other Rabi pulses', 'Other Summer Pulses', 'Peas & beans (Pulses)', 'Cowpea(Lobia)', 'Horse-gram', 'Khesari', 'Moth'],
        'oilseeds': ['Groundnut', 'Sesamum', 'Rapeseed & Mustard', 'Linseed', 'Castor seed', 'Safflower', 'Niger seed', 'Soyabean', 'Sunflower', 'Other oilseeds', 'Oilseeds total'],
        'vegetables': ['Potato', 'Onion', 'Tapioca', 'Sweet potato', 'Garlic'],
        'spices': ['Ginger', 'Turmeric', 'Dry chillies', 'Black pepper', 'Cardamom', 'Coriander'],
        'commercial': ['Cotton(lint)', 'Jute', 'Sugarcane', 'Tobacco', 'Mesta', 'Sannhamp'],
        'fruits': ['Banana', 'Coconut', 'Arecanut', 'Cashewnut']
    }
    
    # Determine crop category
    crop_category = None
    for category, crops in crop_categories.items():
        if crop in crops:
            crop_category = category
            break
    
    # Default values
    fertilizer = 100
    pesticide = 1.0
    
    # Adjust based on category
    if crop_category == 'cereals':
        fertilizer = 120 * state_multiplier
        pesticide = 1.2 * state_multiplier
    elif crop_category == 'pulses':
        fertilizer = 60 * state_multiplier
        pesticide = 1.0 * state_multiplier
    elif crop_category == 'oilseeds':
        fertilizer = 80 * state_multiplier
        pesticide = 1.5 * state_multiplier
    elif crop_category == 'vegetables':
        fertilizer = 200 * state_multiplier
        pesticide = 2.0 * state_multiplier
    elif crop_category == 'spices':
        fertilizer = 150 * state_multiplier
        pesticide = 2.5 * state_multiplier
    elif crop_category == 'commercial':
        fertilizer = 180 * state_multiplier
        pesticide = 3.0 * state_multiplier
    elif crop_category == 'fruits':
        fertilizer = 250 * state_multiplier
        pesticide = 2.0 * state_multiplier
    
    # Calculate production
    production = predicted_yield * area
    
    return {
        'yield': predicted_yield,
        'production': production,
        'rainfall': rainfall,
        'fertilizer': fertilizer,
        'pesticide': pesticide
    }

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        crop_year = int(request.form['Crop_Year'])
        state = request.form['State']
        season = request.form['Season']
        crop = request.form['Crop']
        area = float(request.form['Area'])
        
        # Get prediction
        prediction = predict_crop_yield(crop, crop_year, state, season, area)
        
        # Get price per ton
        price_per_ton = CROP_PRICES.get(crop, 10000)
        
        # Calculate investment and profit
        fertilizer_cost = prediction['fertilizer'] * 20  # ₹20 per kg of fertilizer
        pesticide_cost = prediction['pesticide'] * 300   # ₹300 per kg of pesticide
        labor_cost = 3000                                # ₹3000 fixed labor cost per hectare
        
        investment_per_hectare = fertilizer_cost + pesticide_cost + labor_cost
        investment = area * investment_per_hectare
        profit = (prediction['yield'] * area * price_per_ton) - investment
        
        return render_template_string(
            HTML_TEMPLATE,
            predicted_value=round(prediction['yield'], 2),
            production=round(prediction['production'], 2),
            rainfall=round(prediction['rainfall'], 2),
            fertilizer=round(prediction['fertilizer'], 2),
            pesticide=round(prediction['pesticide'], 2),
            price_per_ton=price_per_ton,
            investment=round(investment, 2),
            profit=round(profit, 2)
        )
        
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, error=f"Error: {str(e)}")

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    try:
        # Get form data
        crop_year = int(request.form['crop_year'])
        state = request.form['state']
        season = request.form['season']
        crop = request.form['crop']
        area = float(request.form['area'])

        # Get prediction
        prediction = predict_crop_yield(crop, crop_year, state, season, area)

        # Get price per ton
        price_per_ton = CROP_PRICES.get(crop, 10000)

        # Calculate investment and profit
        fertilizer_cost = prediction['fertilizer'] * 20  # ₹20 per kg of fertilizer
        pesticide_cost = prediction['pesticide'] * 300   # ₹300 per kg of pesticide
        labor_cost = 3000                                # ₹3000 fixed labor cost per hectare

        investment_per_hectare = fertilizer_cost + pesticide_cost + labor_cost
        investment = area * investment_per_hectare
        profit = (prediction['yield'] * area * price_per_ton) - investment

        # Render the HTML with prediction data
        rendered_html = f"""
        <html>
        <head><title>Prediction Report</title></head>
        <body>
            <h1>Prediction Report</h1>
            <p><strong>Farmer's Name:</strong> {request.form.get('farmer_name', 'N/A')}</p>
            <p><strong>Crop Year:</strong> {crop_year}</p>
            <p><strong>State:</strong> {state}</p>
            <p><strong>Season:</strong> {season}</p>
            <p><strong>Crop:</strong> {crop}</p>
            <p><strong>Area:</strong> {area} hectares</p>
            <h2>Prediction Results</h2>
            <ul>
                <li><strong>Predicted Yield:</strong> {round(prediction['yield'], 2)} tons/hectare</li>
                <li><strong>Production:</strong> {round(prediction['production'], 2)} tons</li>
                <li><strong>Annual Rainfall:</strong> {round(prediction['rainfall'], 2)} mm</li>
                <li><strong>Fertilizer:</strong> {round(prediction['fertilizer'], 2)} kg/hectare</li>
                <li><strong>Pesticide:</strong> {round(prediction['pesticide'], 2)} kg/hectare</li>
                <li><strong>Price per Ton:</strong> ₹{price_per_ton}</li>
                <li><strong>Investment:</strong> ₹{round(investment, 2)}</li>
                <li><strong>Profit:</strong> ₹{round(profit, 2)}</li>
            </ul>
        </body>
        </html>
        """

        # Convert the rendered HTML to PDF
        pdf = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.StringIO(rendered_html), dest=pdf)

        if pisa_status.err:
            return "Error generating PDF", 500

        # Return the PDF as a downloadable file
        pdf.seek(0)
        return send_file(pdf, as_attachment=True, download_name='prediction_report.pdf', mimetype='application/pdf')

    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/favicon.ico')
def favicon():
    return "", 204

if __name__ == '__main__':
    # Use port 5000 by default, but allow it to be set by environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)