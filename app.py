from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, BooleanField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional
from flask_wtf.csrf import CSRFProtect
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['WTF_CSRF_ENABLED'] = True
csrf = CSRFProtect(app)

# Form Classes
class MarketPriceForm(FlaskForm):
    crop = SelectField('Crop', validators=[DataRequired()], 
                      choices=[
                          ('', 'Select Crop'),
                          ('rice', 'Rice'),
                          ('wheat', 'Wheat'),
                          ('maize', 'Maize'),
                          ('sugarcane', 'Sugarcane'),
                          ('cotton', 'Cotton')
                      ])
    variety = StringField('Variety', validators=[DataRequired()])
    quantity = IntegerField('Quantity (quintals)', validators=[DataRequired(), NumberRange(min=1)])
    location = StringField('Location', validators=[DataRequired()])
    harvest_date = StringField('Expected Harvest Date', validators=[DataRequired()])

class CropRecommendationForm(FlaskForm):
    # Location Details
    state = SelectField('State', validators=[DataRequired()],
                      choices=[
                          ('', 'Select State'),
                          ('Andhra Pradesh', 'Andhra Pradesh'),
                          ('Karnataka', 'Karnataka'),
                          ('Kerala', 'Kerala'),
                          ('Tamil Nadu', 'Tamil Nadu'),
                          ('Telangana', 'Telangana'),
                          ('Maharashtra', 'Maharashtra'),
                          ('Gujarat', 'Gujarat'),
                          ('Punjab', 'Punjab'),
                          ('Haryana', 'Haryana'),
                          ('Uttar Pradesh', 'Uttar Pradesh'),
                          ('Madhya Pradesh', 'Madhya Pradesh'),
                          ('Rajasthan', 'Rajasthan'),
                          ('West Bengal', 'West Bengal'),
                          ('Bihar', 'Bihar'),
                          ('Odisha', 'Odisha')
                      ])
    district = StringField('District', validators=[DataRequired()])
    
    # Soil Properties
    soil_type = SelectField('Soil Type', validators=[DataRequired()],
                          choices=[
                              ('', 'Select Soil Type'),
                              ('black', 'Black'),
                              ('red', 'Red'),
                              ('sandy', 'Sandy'),
                              ('clay', 'Clay'),
                              ('loamy', 'Loamy')
                          ])
    ph_level = DecimalField('pH Level', validators=[DataRequired(), NumberRange(min=0, max=14)])
    
    # Nutrient Levels
    nitrogen = IntegerField('Nitrogen (kg/ha)', validators=[DataRequired(), NumberRange(min=0)])
    phosphorus = IntegerField('Phosphorus (kg/ha)', validators=[DataRequired(), NumberRange(min=0)])
    potassium = IntegerField('Potassium (kg/ha)', validators=[DataRequired(), NumberRange(min=0)])
    
    # Climate Conditions
    rainfall = IntegerField('Annual Rainfall (mm)', validators=[DataRequired(), NumberRange(min=0)])
    temperature = DecimalField('Average Temperature (°C)', validators=[DataRequired()])
    humidity = IntegerField('Humidity (%)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    
    # Irrigation
    irrigation = SelectField('Irrigation', validators=[DataRequired()],
                           choices=[
                               ('', 'Select Irrigation'),
                               ('yes', 'Yes'),
                               ('no', 'No')
                           ])

class SchemeEligibilityForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=100)])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    state = StringField('State', validators=[DataRequired()])
    district = StringField('District', validators=[DataRequired()])
    land_ownership = SelectField('Land Ownership', 
                               choices=[
                                   ('own', 'Owned'),
                                   ('lease', 'Leased'),
                                   ('none', 'Landless')
                               ],
                               validators=[DataRequired()])
    land_size = DecimalField('Land Size (acres)', validators=[Optional(), NumberRange(min=0)])
    annual_income = IntegerField('Annual Income (₹)', validators=[DataRequired(), NumberRange(min=0)])
    caste_category = SelectField('Caste Category',
                               choices=[
                                   ('general', 'General'),
                                   ('obc', 'OBC'),
                                   ('sc', 'SC'),
                                   ('st', 'ST')
                               ],
                               validators=[DataRequired()])
    bank_account = SelectField('Do you have a bank account?',
                             choices=[
                                 ('yes', 'Yes'),
                                 ('no', 'No')
                             ],
                             validators=[DataRequired()])
    aadhaar_linked = SelectField('Is your Aadhaar linked to bank account?',
                                choices=[
                                    ('yes', 'Yes'),
                                    ('no', 'No')
                                ],
                                validators=[DataRequired()])

class DisasterPredictionForm(FlaskForm):
    state = SelectField('State', validators=[DataRequired()], 
                       choices=[
                           ('', 'Select State'),
                           ('Andhra Pradesh', 'Andhra Pradesh'),
                           ('Karnataka', 'Karnataka'),
                           ('Kerala', 'Kerala'),
                           ('Tamil Nadu', 'Tamil Nadu'),
                           ('Maharashtra', 'Maharashtra')
                       ])
    district = StringField('District', validators=[DataRequired()])
    crop_type = SelectField('Crop Type', validators=[DataRequired()],
                          choices=[
                              ('', 'Select Crop'),
                              ('rice', 'Rice'),
                              ('wheat', 'Wheat'),
                              ('maize', 'Maize'),
                              ('sugarcane', 'Sugarcane'),
                              ('cotton', 'Cotton'),
                              ('pulses', 'Pulses'),
                              ('vegetables', 'Vegetables'),
                              ('fruits', 'Fruits')
                          ])
    growth_stage = SelectField('Growth Stage', validators=[DataRequired()],
                             choices=[
                                 ('', 'Select Stage'),
                                 ('sowing', 'Sowing'),
                                 ('vegetative', 'Vegetative'),
                                 ('flowering', 'Flowering'),
                                 ('fruiting', 'Fruiting'),
                                 ('maturity', 'Maturity')
                             ])
    soil_moisture = SelectField('Soil Moisture',
                               choices=[
                                   ('dry', 'Dry'),
                                   ('normal', 'Normal'),
                                   ('wet', 'Wet'),
                                   ('waterlogged', 'Waterlogged')
                               ],
                               default='normal')
    weather_forecast = SelectField('Weather Forecast',
                                  choices=[
                                      ('clear', 'Clear Skies'),
                                      ('partly_cloudy', 'Partly Cloudy'),
                                      ('cloudy', 'Cloudy'),
                                      ('rain', 'Rain Expected'),
                                      ('heavy_rain', 'Heavy Rain Expected'),
                                      ('drought', 'Drought Conditions')
                                  ],
                                  default='clear')
    temperature = DecimalField('Temperature (°C)', validators=[DataRequired()], default=28.0)
    pest_infestation = BooleanField('Pest Infestation')
    disease_signs = BooleanField('Disease Signs')
    weed_problem = BooleanField('Weed Problem')
    observations = TextAreaField('Additional Observations')

# Crop Recommendation Dataset
CROP_RECOMMENDATION_DATA = {
    # For Black Soil
    'black': {
        'high_rainfall': ['Cotton', 'Soybean', 'Sugarcane', 'Groundnut'],
        'medium_rainfall': ['Wheat', 'Chickpea', 'Sunflower', 'Maize'],
        'low_rainfall': ['Pearl Millet', 'Sorghum', 'Pigeon Pea']
    },
    # For Red Soil
    'red': {
        'high_rainfall': ['Rice', 'Sugarcane', 'Banana', 'Coconut'],
        'medium_rainfall': ['Groundnut', 'Potato', 'Ragi', 'Tobacco'],
        'low_rainfall': ['Pearl Millet', 'Horse Gram', 'Castor']
    },
    # For Sandy Soil
    'sandy': {
        'high_rainfall': ['Watermelon', 'Cucumber', 'Pumpkin'],
        'medium_rainfall': ['Groundnut', 'Sunflower', 'Potato'],
        'low_rainfall': ['Pearl Millet', 'Cluster Beans', 'Moth Beans']
    },
    # For Clay Soil
    'clay': {
        'high_rainfall': ['Rice', 'Wheat', 'Soybean'],
        'medium_rainfall': ['Chickpea', 'Lentil', 'Barley'],
        'low_rainfall': ['Sorghum', 'Pearl Millet', 'Cowpea']
    },
    # For Loamy Soil
    'loamy': {
        'high_rainfall': ['Rice', 'Wheat', 'Sugarcane', 'Cotton'],
        'medium_rainfall': ['Maize', 'Soybean', 'Groundnut'],
        'low_rainfall': ['Pearl Millet', 'Green Gram', 'Black Gram']
    }
}

# Government Schemes Dataset
GOVERNMENT_SCHEMES = [
    {
        'name': 'PM-KISAN',
        'description': 'Income support of ₹6,000 per year to all farmer families across the country in three equal installments of ₹2,000 each every four months.',
        'eligibility': {
            'land_ownership': ['own', 'lease'],
            'land_size': None,  # No minimum land size
            'annual_income': 100000,  # Maximum annual income
            'caste_category': ['general', 'obc', 'sc', 'st'],
            'bank_account': True,
            'aadhaar_linked': True
        },
        'benefits': '₹6,000 per year in three installments',
        'apply_link': 'https://pmkisan.gov.in/'
    },
    {
        'name': 'PM Fasal Bima Yojana',
        'description': 'Crop insurance scheme to provide financial support to farmers suffering crop loss/damage arising out of unforeseen events.',
        'eligibility': {
            'land_ownership': ['own', 'lease'],
            'land_size': None,  # No minimum land size
            'annual_income': None,  # No income limit
            'caste_category': ['general', 'obc', 'sc', 'st'],
            'bank_account': True,
            'aadhaar_linked': True
        },
        'benefits': 'Premium: 2% for Kharif, 1.5% for Rabi, 5% for commercial/horticultural crops',
        'apply_link': 'https://pmfby.gov.in/'
    },
    {
        'name': 'Kisan Credit Card (KCC)',
        'description': 'Provides farmers with timely access to credit for their agricultural needs at a reduced interest rate.',
        'eligibility': {
            'land_ownership': ['own', 'lease'],
            'land_size': None,  # No minimum land size
            'annual_income': None,  # No income limit
            'caste_category': ['general', 'obc', 'sc', 'st'],
            'bank_account': True,
            'aadhaar_linked': True
        },
        'benefits': 'Interest subvention of 2% per annum and prompt repayment incentive of 3% per annum',
        'apply_link': 'https://www.indiagov.in/schemes/kisan-credit-card-kcc'
    },
    {
        'name': 'National Mission for Sustainable Agriculture (NMSA)',
        'description': 'Promotes sustainable agriculture through climate change adaptation measures, and location-specific integrated farming systems.',
        'eligibility': {
            'land_ownership': ['own', 'lease'],
            'land_size': 0.5,  # Minimum 0.5 acres
            'annual_income': 100000,  # Maximum annual income
            'caste_category': ['sc', 'st', 'obc'],
            'bank_account': True,
            'aadhaar_linked': True
        },
        'benefits': 'Financial assistance up to 50-100% of the cost of various components',
        'apply_link': 'https://nmsa.dac.gov.in/'
    },
    {
        'name': 'Soil Health Card Scheme',
        'description': 'Provides soil health cards to farmers which carry crop-wise recommendations of nutrients and fertilizers required for their farms.',
        'eligibility': {
            'land_ownership': ['own', 'lease'],
            'land_size': None,  # No minimum land size
            'annual_income': None,  # No income limit
            'caste_category': ['general', 'obc', 'sc', 'st'],
            'bank_account': False,  # Not required
            'aadhaar_linked': False  # Not required
        },
        'benefits': 'Free soil testing and recommendations every 2 years',
        'apply_link': 'https://soilhealth.dac.gov.in/'
    }
]

# Mock data and functions
def get_market_price(crop, variety, quantity, location, harvest_date):
    # Mock implementation - replace with actual prediction logic
    return {
        'predicted_price': f"₹4,200 - ₹4,800 per quintal",
        'nearest_mandi': f"{location} APMC Market"
    }

def get_historical_prices(crop, location):
    """
    Generate mock historical price data for the chart
    In a real application, this would query your database or API
    """
    import random
    from datetime import datetime, timedelta
    
    # Generate data for the last 6 months
    months = []
    prices = []
    today = datetime.now()
    
    # Base price varies by crop (for demo purposes)
    base_prices = {
        'rice': 4500,
        'wheat': 4000,
        'maize': 3800,
        'sugarcane': 3500,
        'cotton': 5500,
    }
    
    base_price = base_prices.get(crop.lower(), 4000)  # Default to 4000 if crop not found
    
    for i in range(5, -1, -1):
        # Calculate date for each month
        date = today - timedelta(days=30*i)
        months.append(date.strftime('%b %Y'))
        
        # Generate price with some variation
        variation = random.uniform(-0.15, 0.15)  # +/- 15% variation
        price = base_price * (1 + variation)
        prices.append(round(price, 2))
    
    return {
        'months': months,
        'prices': prices,
        'current_price': prices[-1],
        'price_change': round(((prices[-1] - prices[0]) / prices[0]) * 100, 1) if prices[0] != 0 else 0
    }

def get_crop_recommendation(soil_type, ph_level, rainfall, temperature):
    """
    Get crop recommendations based on soil type, pH level, rainfall, and temperature.
    Returns a list of recommended crops sorted by suitability.
    """
    # Comprehensive crop database with detailed requirements
    CROPS = {
        'Pearl Millet (Bajra)': {
            'soil': ['sandy', 'sandy loam', 'loamy'],
            'ph_range': (6.0, 7.5),
            'rainfall': (200, 600),
            'temperature': (25, 35),
            'drought_tolerant': True,
            'description': 'Highly drought-resistant cereal crop that grows well in low rainfall areas.'
        },
        'Sorghum (Jowar)': {
            'soil': ['sandy loam', 'loamy', 'clay loam'],
            'ph_range': (5.5, 8.5),
            'rainfall': (300, 650),
            'temperature': (25, 32),
            'drought_tolerant': True,
            'description': 'Drought-resistant crop, good for arid and semi-arid regions.'
        },
        'Chickpea (Chana)': {
            'soil': ['sandy loam', 'loamy', 'black cotton'],
            'ph_range': (6.0, 8.0),
            'rainfall': (250, 600),
            'temperature': (20, 30),
            'drought_tolerant': True,
            'description': 'Legume crop that fixes nitrogen and is drought-tolerant.'
        },
        'Pigeon Pea (Arhar/Toor)': {
            'soil': ['sandy loam', 'loamy', 'red'],
            'ph_range': (6.0, 7.5),
            'rainfall': (250, 800),
            'temperature': (20, 35),
            'drought_tolerant': True,
            'description': 'Deep-rooted legume, good for dryland farming.'
        },
        'Moth Bean': {
            'soil': ['sandy', 'sandy loam'],
            'ph_range': (6.0, 8.0),
            'rainfall': (200, 500),
            'temperature': (25, 38),
            'drought_tolerant': True,
            'description': 'One of the most drought-resistant pulses, grows in arid conditions.'
        },
        'Cluster Bean (Guar)': {
            'soil': ['sandy', 'sandy loam'],
            'ph_range': (6.0, 8.5),
            'rainfall': (150, 450),
            'temperature': (25, 40),
            'drought_tolerant': True,
            'description': 'Highly drought-resistant, used for vegetable, fodder, and guar gum.'
        },
        'Castor': {
            'soil': ['sandy loam', 'loamy', 'clay loam'],
            'ph_range': (5.0, 8.5),
            'rainfall': (200, 500),
            'temperature': (20, 35),
            'drought_tolerant': True,
            'description': 'Oilseed crop that can grow in poor soils with low rainfall.'
        },
        'Sesame (Til)': {
            'soil': ['sandy loam', 'loamy'],
            'ph_range': (5.5, 8.0),
            'rainfall': (200, 500),
            'temperature': (25, 35),
            'drought_tolerant': True,
            'description': 'Drought-resistant oilseed crop, grows well in hot conditions.'
        },
        'Cowpea (Lobia)': {
            'soil': ['sandy', 'sandy loam', 'loamy'],
            'ph_range': (5.5, 7.5),
            'rainfall': (250, 700),
            'temperature': (20, 35),
            'drought_tolerant': True,
            'description': 'Heat and drought-tolerant legume, good for dry regions.'
        },
        'Mung Bean (Green Gram)': {
            'soil': ['sandy loam', 'loamy'],
            'ph_range': (6.0, 7.5),
            'rainfall': (250, 600),
            'temperature': (25, 35),
            'drought_tolerant': True,
            'description': 'Short-duration crop, relatively drought-resistant.'
        }
    }
    
    # Normalize soil type for comparison
    soil_type = soil_type.lower().strip()
    
    # Calculate score for each crop
    crop_scores = {}
    
    for crop, reqs in CROPS.items():
        score = 0
        
        # Check soil type (3 points)
        if any(soil in soil_type for soil in reqs['soil']):
            score += 3
            
        # Check pH level (2 points)
        min_ph, max_ph = reqs['ph_range']
        if min_ph <= ph_level <= max_ph:
            score += 2
        else:
            # Partial points for close pH
            if min_ph - 0.5 <= ph_level < min_ph or max_ph < ph_level <= max_ph + 0.5:
                score += 1
            
        # Check rainfall (2 points)
        min_rain, max_rain = reqs['rainfall']
        if min_rain <= rainfall <= max_rain:
            score += 2
        else:
            # Partial points for close rainfall
            if min_rain * 0.8 <= rainfall < min_rain or max_rain < rainfall <= max_rain * 1.2:
                score += 1
        
        # Check temperature (2 points)
        min_temp, max_temp = reqs['temperature']
        if min_temp <= temperature <= max_temp:
            score += 2
        else:
            # Partial points for close temperature
            if min_temp - 2 <= temperature < min_temp or max_temp < temperature <= max_temp + 2:
                score += 1
        
        # Additional points for drought tolerance (since rainfall is very low)
        if reqs.get('drought_tolerant', False):
            score += 2
        
        # Store the score if it's above threshold
        if score >= 3:  # At least one requirement must be fully met
            crop_scores[crop] = {
                'score': score,
                'description': reqs.get('description', '')
            }
    
    # Sort crops by score in descending order
    sorted_crops = sorted(crop_scores.items(), key=lambda x: x[1]['score'], reverse=True)
    
    # Return list of crops with their details
    return [{
        'name': crop,
        'description': details['description']
    } for crop, details in sorted_crops]

def check_scheme_eligibility(form_data):
    """
    Check eligibility for government schemes based on farmer's details
    """
    # Define government schemes with eligibility criteria
    SCHEMES = [
        {
            'name': 'PM-KISAN',
            'description': 'Income support of ₹6,000 per year to all farmer families',
            'eligibility': {
                'land_ownership': ['own', 'lease'],
                'annual_income_max': 150000,
                'caste_category': ['general', 'obc', 'sc', 'st'],
                'bank_account': True,
                'aadhaar_linked': True
            },
            'benefits': '₹6,000 per year in three installments',
            'website': 'https://pmkisan.gov.in/'
        },
        {
            'name': 'PM Fasal Bima Yojana',
            'description': 'Crop insurance scheme to protect against crop failure',
            'eligibility': {
                'land_ownership': ['own', 'lease'],
                'crop_type': True,  # Any crop
                'bank_account': True,
                'aadhaar_linked': True
            },
            'benefits': 'Insurance coverage for crop failure',
            'website': 'https://pmfby.gov.in/'
        },
        {
            'name': 'Kisan Credit Card (KCC)',
            'description': 'Easy credit access for farmers',
            'eligibility': {
                'land_ownership': ['own', 'lease'],
                'age_min': 18,
                'age_max': 75,
                'bank_account': True,
                'aadhaar_linked': True
            },
            'benefits': 'Low-interest loans up to ₹3 lakh',
            'website': 'https://www.iffcobank.com/kisan-credit-card.html'
        },
        {
            'name': 'Soil Health Card Scheme',
            'description': 'Provides soil health cards to farmers',
            'eligibility': {
                'all_farmers': True
            },
            'benefits': 'Free soil testing and recommendations',
            'website': 'https://soilhealth.dac.gov.in/'
        },
        {
            'name': 'National Mission for Sustainable Agriculture',
            'description': 'Promotes sustainable agriculture practices',
            'eligibility': {
                'land_ownership': ['own', 'lease'],
                'annual_income_max': 500000
            },
            'benefits': 'Subsidy on seeds, equipment, and training',
            'website': 'https://nmsa.dac.gov.in/'
        }
    ]
    
    eligible_schemes = []
    
    for scheme in SCHEMES:
        is_eligible = True
        
        # Check each eligibility criterion
        for key, req_value in scheme['eligibility'].items():
            if key == 'all_farmers' and req_value:
                continue  # All farmers are eligible
                
            if key == 'land_ownership':
                if form_data['land_ownership'] not in req_value:
                    is_eligible = False
                    break
                    
            elif key == 'annual_income_max':
                if form_data['annual_income'] > req_value:
                    is_eligible = False
                    break
                    
            elif key == 'caste_category':
                if form_data['caste_category'] not in req_value:
                    is_eligible = False
                    break
                    
            elif key in ['bank_account', 'aadhaar_linked']:
                if not form_data[key]:
                    is_eligible = False
                    break
                    
            elif key == 'age_min':
                if form_data['age'] < req_value:
                    is_eligible = False
                    break
                    
            elif key == 'age_max':
                if form_data['age'] > req_value:
                    is_eligible = False
                    break
        
        if is_eligible:
            eligible_schemes.append(scheme)
    
    return eligible_schemes

def predict_disaster_risk(form_data):
    """
    Mock function to simulate disaster risk prediction.
    In a real application, this would use ML models and weather APIs.
    """
    # Base risk level (low, moderate, high)
    risk_level = "Low"
    potential_threats = []
    preventive_measures = []
    
    # Analyze weather conditions
    if form_data['weather_forecast'] in ['heavy_rain', 'drought']:
        risk_level = "High"
        if form_data['weather_forecast'] == 'heavy_rain':
            potential_threats.append("Heavy rainfall may cause waterlogging and flooding")
            preventive_measures.append("Ensure proper drainage in fields")
            preventive_measures.append("Harvest mature crops if possible")
        else:  # drought
            potential_threats.append("Drought conditions may affect crop growth")
            preventive_measures.append("Implement water conservation techniques")
            preventive_measures.append("Consider drought-resistant crop varieties")
    
    # Analyze temperature
    temp = float(form_data['temperature'])
    if temp > 35:
        risk_level = "Moderate" if risk_level == "Low" else risk_level
        potential_threats.append(f"High temperature ({temp}°C) may cause heat stress")
        preventive_measures.append("Ensure adequate irrigation")
        preventive_measures.append("Apply mulch to conserve soil moisture")
    elif temp < 10:
        risk_level = "Moderate" if risk_level == "Low" else risk_level
        potential_threats.append(f"Low temperature ({temp}°C) may cause cold stress")
        preventive_measures.append("Cover sensitive crops with frost blankets")
    
    # Analyze soil moisture
    if form_data['soil_moisture'] == 'dry':
        potential_threats.append("Dry soil conditions detected")
        preventive_measures.append("Irrigate fields as needed")
    elif form_data['soil_moisture'] == 'waterlogged':
        risk_level = "Moderate" if risk_level == "Low" else risk_level
        potential_threats.append("Waterlogged soil may damage roots")
        preventive_measures.append("Improve field drainage")
    
    # Check for pests and diseases
    if form_data.get('pest_infestation'):
        risk_level = "Moderate" if risk_level == "Low" else risk_level
        potential_threats.append("Pest infestation detected")
        preventive_measures.append("Inspect crops for pest damage")
        preventive_measures.append("Consider organic or chemical pest control methods")
    
    if form_data.get('disease_signs'):
        risk_level = "Moderate" if risk_level == "Low" else risk_level
        potential_threats.append("Signs of plant disease detected")
        preventive_measures.append("Identify the specific disease")
        preventive_measures.append("Apply appropriate fungicides if necessary")
    
    if form_data.get('weed_problem'):
        potential_threats.append("Weed competition detected")
        preventive_measures.append("Remove weeds manually or with appropriate herbicides")
    
    # Add general preventive measures
    preventive_measures.append("Monitor weather forecasts regularly")
    preventive_measures.append("Inspect crops frequently for signs of stress or disease")
    
    # Generate mock weather forecast (7 days)
    weather_forecast = []
    for i in range(7):
        date = (datetime.now() + timedelta(days=i)).strftime("%a, %b %d")
        weather_forecast.append({
            'date': date,
            'condition': 'Sunny' if i % 3 != 2 else 'Rainy',
            'icon': 'sun' if i % 3 != 2 else 'cloud-rain',
            'high': 32 + random.randint(-2, 3),
            'low': 22 + random.randint(-2, 3),
            'rain_chance': 10 if i % 3 != 2 else 70 + random.randint(0, 25),
            'wind_speed': f"{5 + random.randint(0, 10)}-{15 + random.randint(0, 10)}"
        })
    
    # Determine next steps based on risk level
    if risk_level == "High":
        next_steps = "Take immediate action to protect your crops. Consider consulting an agricultural expert."
    elif risk_level == "Moderate":
        next_steps = "Monitor conditions closely and implement preventive measures as needed."
    else:
        next_steps = "Continue with regular monitoring and maintenance."
    
    # Add any observations to potential threats
    if form_data.get('observations'):
        potential_threats.append(f"Note: {form_data['observations']}")
    
    # If no specific threats found, add a general message
    if not potential_threats:
        potential_threats = ["No immediate threats detected. Continue regular monitoring."]
    
    return {
        'risk_level': risk_level,
        'potential_threats': potential_threats[:5],  # Limit to top 5 threats
        'preventive_measures': list(dict.fromkeys(preventive_measures))[:6],  # Remove duplicates and limit to 6
        'next_steps': next_steps,
        'weather_forecast': weather_forecast,
        'location': f"{form_data['district']}, {form_data['state']}",
        'crop': dict(DisasterPredictionForm().crop_type.choices).get(form_data['crop_type']),
        'growth_stage': dict(DisasterPredictionForm().growth_stage.choices).get(form_data['growth_stage'])
    }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/market-price', methods=['GET', 'POST'])
def market_price():
    form = MarketPriceForm()
    result = None
    chart_data = None
    
    if form.validate_on_submit():
        # Get form data
        crop = form.crop.data
        variety = form.variety.data
        quantity = form.quantity.data
        location = form.location.data
        harvest_date = form.harvest_date.data
        
        # Get price prediction (mock)
        predicted_price = {
            'predicted_price': f"₹4,200 - ₹4,800 per quintal",
            'nearest_mandi': f"{location} APMC Market",
            'crop': crop,
            'location': location
        }
        
        # Get historical price data for the chart
        historical_data = get_historical_prices(crop, location)
        
        # Combine all data
        result = {
            **predicted_price,
            'historical_data': historical_data
        }
        
        # Prepare chart data for JavaScript
        chart_data = {
            'labels': historical_data['months'],
            'prices': historical_data['prices'],
            'current_price': historical_data['current_price'],
            'price_change': historical_data['price_change']
        }
    
    return render_template('market_price.html', 
                         form=form, 
                         result=result,
                         chart_data=chart_data)

@app.route('/crop-recommendation', methods=['GET', 'POST'])
def crop_recommendation():
    form = CropRecommendationForm()
    
    if request.method == 'POST':
        print("\n=== Form Submission Debugging ===")
        print("Form submitted!")
        print("Form data:", request.form)
        print("Form errors:", form.errors)
        
        if form.validate_on_submit():
            print("Form validation successful!")
            # Get form data from the form object
            state = form.state.data
            district = form.district.data
            soil_type = form.soil_type.data
            ph = float(form.ph_level.data)
            nitrogen = int(form.nitrogen.data)
            phosphorus = int(form.phosphorus.data)
            potassium = int(form.potassium.data)
            rainfall = int(form.rainfall.data)
            temperature = float(form.temperature.data)
            humidity = int(form.humidity.data)
            
            print("\n=== Form Data Extracted ===")
            print(f"State: {state}, District: {district}")
            print(f"Soil: {soil_type}, pH: {ph}, N: {nitrogen}, P: {phosphorus}, K: {potassium}")
            print(f"Climate: {temperature}°C, {rainfall}mm, {humidity}%")
            
            # Get crop recommendations
            crop_recommendations = get_crop_recommendation(
                soil_type=soil_type,
                ph_level=ph,
                rainfall=rainfall,
                temperature=temperature
            )
            
            print("\n=== Crop Recommendations ===")
            print("Recommended crops:", crop_recommendations)
            
            # Define crop data for the template
            CROP_DATA = {
                'Pearl Millet (Bajra)': {
                    'soil': 'Sandy, Loamy',
                    'temperature': '25-35°C',
                    'rainfall': '200-600mm',
                    'ph_range': '6.0-7.5',
                    'description': 'Highly drought-resistant cereal crop that grows well in low rainfall areas.'
                },
                'Sorghum (Jowar)': {
                    'soil': 'Sandy Loam, Loamy, Clay Loam',
                    'temperature': '25-32°C',
                    'rainfall': '300-650mm',
                    'ph_range': '5.5-8.5',
                    'description': 'Drought-resistant crop, good for arid and semi-arid regions.'
                },
                'Chickpea (Chana)': {
                    'soil': 'Sandy Loam, Loamy, Black Cotton',
                    'temperature': '20-30°C',
                    'rainfall': '250-600mm',
                    'ph_range': '6.0-8.0',
                    'description': 'Legume crop that fixes nitrogen and is drought-tolerant.'
                },
                'Pigeon Pea (Arhar/Toor)': {
                    'soil': 'Sandy Loam, Loamy, Red',
                    'temperature': '20-35°C',
                    'rainfall': '250-800mm',
                    'ph_range': '6.0-7.5',
                    'description': 'Deep-rooted legume, good for dryland farming.'
                },
                'Moth Bean': {
                    'soil': 'Sandy, Sandy Loam',
                    'temperature': '25-38°C',
                    'rainfall': '200-500mm',
                    'ph_range': '6.0-8.0',
                    'description': 'One of the most drought-resistant pulses, grows in arid conditions.'
                },
                'Cluster Bean (Guar)': {
                    'soil': 'Sandy, Sandy Loam',
                    'temperature': '25-40°C',
                    'rainfall': '150-450mm',
                    'ph_range': '6.0-8.5',
                    'description': 'Highly drought-resistant, used for vegetable, fodder, and guar gum.'
                },
                'Castor': {
                    'soil': 'Sandy Loam, Loamy, Clay Loam',
                    'temperature': '20-35°C',
                    'rainfall': '200-500mm',
                    'ph_range': '5.0-8.5',
                    'description': 'Oilseed crop that can grow in poor soils with low rainfall.'
                },
                'Sesame (Til)': {
                    'soil': 'Sandy Loam, Loamy',
                    'temperature': '25-35°C',
                    'rainfall': '200-500mm',
                    'ph_range': '5.5-8.0',
                    'description': 'Drought-resistant oilseed crop, grows well in hot conditions.'
                },
                'Cowpea (Lobia)': {
                    'soil': 'Sandy, Sandy Loam, Loamy',
                    'temperature': '20-35°C',
                    'rainfall': '250-700mm',
                    'ph_range': '5.5-7.5',
                    'description': 'Heat and drought-tolerant legume, good for dry regions.'
                },
                'Mung Bean (Green Gram)': {
                    'soil': 'Sandy Loam, Loamy',
                    'temperature': '25-35°C',
                    'rainfall': '250-600mm',
                    'ph_range': '6.0-7.5',
                    'description': 'Short-duration crop, relatively drought-resistant.'
                }
            }
            
            # Create list of recommended crops with their data
            recommendations = []
            for crop_info in crop_recommendations:
                crop_name = crop_info['name']
                if crop_name in CROP_DATA:
                    crop_data = CROP_DATA[crop_name].copy()
                    crop_data['name'] = crop_name  # Ensure name is included
                    recommendations.append(crop_data)
            
            # If no crops matched, add a message
            if not recommendations:
                flash('No suitable crops found for the given conditions. Please adjust your inputs.', 'warning')
            
            return render_template(
                'crop_recommend.html',
                form=form,
                result=True,
                recommendations=recommendations[:5],  # Limit to top 5 recommendations
                soil_analysis={
                    'ph': ph,
                    'nitrogen': nitrogen,
                    'phosphorus': phosphorus,
                    'potassium': potassium
                },
                climate_conditions={
                    'rainfall': rainfall,
                    'temperature': temperature,
                    'humidity': humidity
                },
                location={
                    'state': state,
                    'district': district
                }
            )
        
        else:
            print("\n=== Form Validation Failed ===")
            print("Form errors:", form.errors)
            flash('Please correct the errors in the form.', 'danger')
    
    # For GET request or invalid form, render the form
    return render_template('crop_recommend.html', form=form, result=False)

@app.route('/schemes', methods=['GET', 'POST'])
def schemes():
    form = SchemeEligibilityForm()
    
    if request.method == 'POST':
        # Create a dictionary with form data
        form_data = {
            'name': request.form.get('name'),
            'age': int(request.form.get('age', 0)),
            'gender': request.form.get('gender'),
            'state': request.form.get('state'),
            'district': request.form.get('district'),
            'land_ownership': request.form.get('land_ownership'),
            'land_size': float(request.form.get('land_size', 0)) if request.form.get('land_size') else 0,
            'annual_income': int(request.form.get('annual_income', 0)),
            'caste_category': request.form.get('caste_category'),
            'bank_account': request.form.get('bank_account') == 'yes',
            'aadhaar_linked': request.form.get('aadhaar_linked') == 'yes'
        }
        
        # Check eligibility for schemes
        eligible_schemes = check_scheme_eligibility(form_data)
        
        # Populate the form with submitted data for display
        form.process(data=request.form)
        
        return render_template('schemes.html', 
                             form=form,  # Pass the form object, not the dict
                             result=True,
                             eligible_schemes=eligible_schemes,
                             form_data=form_data)  # Pass form_data separately if needed
    
    # For GET request, render the empty form
    return render_template('schemes.html', form=form, result=False)

@app.route('/disaster', methods=['GET', 'POST'])
def disaster():
    form = DisasterPredictionForm()
    result = None
    
    if form.validate_on_submit():
        # Get form data
        form_data = {
            'state': form.state.data,
            'district': form.district.data,
            'crop_type': form.crop_type.data,
            'growth_stage': form.growth_stage.data,
            'soil_moisture': form.soil_moisture.data,
            'weather_forecast': form.weather_forecast.data,
            'temperature': form.temperature.data,
            'pest_infestation': form.pest_infestation.data,
            'disease_signs': form.disease_signs.data,
            'weed_problem': form.weed_problem.data,
            'observations': form.observations.data
        }
        
        # Get prediction results
        result = predict_disaster_risk(form_data)
    
    return render_template('disaster.html', form=form, result=result)

if __name__ == '__main__':
    app.run(debug=True)
