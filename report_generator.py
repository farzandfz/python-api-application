import pandas as pd
import numpy as np
import boto3
from fpdf import FPDF
from io import BytesIO
import time

# function to generate the report in PDF format
def coverPage(pdf, WIDTH, HEIGHT, NAME, AGE, SEX, CUST_HEIGHT, WEIGHT, LIFESTYLE, FOOD, GOAL, CUST_HEIGHT_FT, BMR, BMI, IDEAL_WEIGHT, CLASS, CALORIES, PROTEIN, CARBS, FATS, FIBER):
    pdf.image("Data/index.jpg", x= 0, y = 0, w= WIDTH, h = HEIGHT)
    
    pdf.ln(30)
    pdf.set_font('Courier', 'B', 18)
    pdf.set_text_color(255,255,255)
    pdf.cell(75, 0, f"Dear {NAME},", align='C')
    
    pdf.set_font('Arial', 'I',  10)
    pdf.ln(6)
    pdf.cell(85, 0, 'Here is a diet recommendation for you',  align='C')
     
    pdf.set_text_color(0,0,0)
    
    pdf.add_font('Poppins', '', "Poppins-Bold.ttf", uni=True)
    pdf.set_font('Poppins', '',  16)
    pdf.ln(56)
    pdf.cell(90, 0, f"                         {NAME}, {SEX}, {AGE} Years",  align='L')
    pdf.cell(90, 0, f"                               {BMR} Kcal",  align='L')
    
    pdf.set_font('Poppins', '',  18)
    pdf.set_text_color(1,109,119)
    pdf.ln(32)
    pdf.cell(85, 0, f"                   {CUST_HEIGHT} cm",  align='L')
    pdf.cell(35, 0, f" {WEIGHT} Kgs",  align='L')
    pdf.cell(65, 0, f"                 {BMI}",  align='L')
    
    
    pdf.set_text_color(0,0,0)
    pdf.set_font('Arial', 'I',  9)
    pdf.ln(6)
    pdf.cell(75, 0, f"                              {CUST_HEIGHT_FT}",  align='L')
    pdf.cell(55, 0, f"            Ideal Weight: {IDEAL_WEIGHT} Kgs",  align='L')
    pdf.cell(85, 0, f"                {CLASS}",  align='L')
    
    
    pdf.set_text_color(0,0,0)
    pdf.set_font('Arial', 'I',  10)
    pdf.ln(15)
    pdf.cell(75, 0, f"                              Activity",  align='L')
    pdf.cell(55, 0, f"               Food choice",  align='L')
    pdf.cell(60, 0, f"                Goal",  align='L')
    
    
    pdf.set_font('Poppins', '',  11)
    pdf.set_text_color(1,109,119)
    pdf.ln(6)
    pdf.cell(75, 0, f"                                   {LIFESTYLE}",  align='L')
    pdf.cell(55, 0, f"                 {FOOD}",  align='L')
    pdf.cell(60, 0, f"                   {GOAL}",  align='L')   
    
    
    pdf.set_font('Poppins', '',  10)
    pdf.set_text_color(0,0,0)
    pdf.ln(51)
    pdf.cell(170, 0, f"                               {CALORIES} Kcal Plan",  align='R')
    
    pdf.set_font('Poppins', '',  13)
    pdf.ln(20.5)
    pdf.cell(50, 0, f"               {PROTEIN} gm",  align='L')
    pdf.cell(40, 0, f"     {CARBS} gm",  align='L')
    pdf.cell(40, 0, f"         {FATS} gm",  align='L')
    pdf.cell(40, 0, f"           {FIBER} gm",  align='L')

# function to convert height in cm to feet
def heightConverter(CUST_HEIGHT):
    heightInFeet = round(CUST_HEIGHT/30.48, 1)
    return str(heightInFeet).split('.')[0]+' feet ' + str(heightInFeet).split('.')[1]+' inch'

# function to calculate the BMI & Ideal Weight
def BMIidealWeightCalculator(WEIGHT, CUST_HEIGHT, SEX):
    # bmi = kg/m2
    heightInMeter = CUST_HEIGHT/100
    bmi = round(WEIGHT/(heightInMeter*heightInMeter), 1)
    
    if bmi <= 18.5:
        tag = 'Underweight'
    elif bmi > 18.5 and bmi <= 24.9:
        tag = 'Normal'
    elif bmi > 25.0 and bmi <= 29.9:
        tag = 'Overweight'
    elif bmi > 30:
        tag = 'Obese'
    
    # G. J. Hamwi Formula (1964)
           # Male:   48.0 kg + 2.7 kg per inch over 5 feet
           # Female: 45.5 kg + 2.2 kg per inch over 5 feet
    
    # ideal weight calculation
    extraHeightInches = (CUST_HEIGHT - 152.4)/2.54
    if SEX == 'Male':
        ibw = 48 + 2.7 * extraHeightInches
    elif SEX == 'Female':
        ibw = 48 + 2.2 * extraHeightInches
    else:
        ibw = 0  
    
    
    return bmi, tag, round(ibw, 1)

# function to calculate BMR
def BMRCalculator(WEIGHT, CUST_HEIGHT, SEX, AGE):
    # Mifflin-St Jeor Equation
            # Male:   BMR = 10W + 6.25H - 5A + 5
            # Female: BMR = 10W + 6.25H - 5A - 161
    
            # W is body weight in kg, H is body height in cm, A is age
        
        # Total daily enegry expenditure
        # TDEE = 1.2 × BMR if you have a sedentary lifestyle (little to no exercise and work a desk job)
        # TDEE = 1.375 × BMR if you have a lightly active lifestyle (light exercise 1-3 days per week)
        # TDEE = 1.55 × BMR if you have a moderately active lifestyle (moderate exercise 3-5 days per week)
        # TDEE = 1.725 × BMR if you have a very active lifestyle (heavy exercise 6-7 days per week)
        # TDEE = 1.9 × BMR if you have an extremely active lifestyle (strenuous training 2 times a day)


    if SEX == 'Male':
        return round(10 * WEIGHT + 6.25 * CUST_HEIGHT - 5 * AGE + 5)

    elif SEX == 'Female':
        return round(10 * WEIGHT + 6.25 * CUST_HEIGHT - 5 * AGE + - 161)

# function to calculate Maintenance Calories
def MaintenanceCalorieCalculator(BMR, LIFESTYLE):
    if LIFESTYLE == 'Sedentary':
        calorie_required = BMR * 1.2
    elif LIFESTYLE == 'Light':
        calorie_required = BMR * 1.375
    elif LIFESTYLE == 'Moderate':
        calorie_required = BMR * 1.465
    elif LIFESTYLE == 'Active':
        calorie_required = BMR * 1.6
    elif LIFESTYLE == 'Very Active':
        calorie_required = BMR * 1.725
    elif LIFESTYLE == 'Extra Active':
        calorie_required = BMR * 1.900
        
    return round(calorie_required)

# function to calculate the final calorie requirement based on customer goals
def ActualCaloriePlan(MAINTENANCE_CALORIE, GOAL, GOAL2):
    
    if GOAL == 'Maintain Weight':
        calorie_required = MAINTENANCE_CALORIE
        
    # 500 gms is roughly equal to 3500 calories which gives a multiplier of 7000
    # if someone wants to loose 250 gm per week, they will have to take away 0.250*7000 or 1750 calorie
    #       per week or 1750/7 per day from BMR
    elif GOAL == 'Loose Weight':
        if GOAL2 == 250:
            calorie_required = MAINTENANCE_CALORIE - ((0.250*7000)/7)
        if GOAL2 == 500:
            calorie_required = MAINTENANCE_CALORIE - ((0.5*7000)/7)
        if GOAL2 == 1000:
            calorie_required = MAINTENANCE_CALORIE - ((1*7000)/7)
            
    elif GOAL == 'Gain Weight':
        if GOAL2 == 250:
            calorie_required = MAINTENANCE_CALORIE + ((0.250*7000)/7)
        if GOAL2 == 500:
            calorie_required = MAINTENANCE_CALORIE + ((0.5*7000)/7)
        if GOAL2 == 1000:
            calorie_required = MAINTENANCE_CALORIE + ((1*7000)/7)
            
    return round(calorie_required)

# function to calculate macros based on customer goals
# 50:25:25 for all three, Maintain, Loose and Gain Weight
def MacroCalculator(MAINTENANCE_CALORIE, CALORIES):
    
    CARBS = round((CALORIES*0.5)/4)
    PROTEIN = round((CALORIES*0.25)/4)
    FATS = round((CALORIES*0.25)/9)
    FIBER = round((MAINTENANCE_CALORIE/1000)*14)
    
    return CARBS, PROTEIN, FATS, FIBER

# NAME = 'Farzand'
# AGE = 27
# SEX = 'Male'
CUST_HEIGHT = 175
WEIGHT = 83
LIFESTYLE = 'Moderate'
FOOD = 'Vegetarian'
GOAL = 'Maintain Weight'
GOAL2 = 250

AWS_ACCESS_KEY_ID = "AKIAXHEQA2NYJE45LYFF"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "healtheirway-files"

# S3 storage system
def store_file(FILENAME, FILESTR):
    s3 = boto3.client('s3', 
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    return s3.upload_file(Bucket=AWS_STORAGE_BUCKET_NAME,
        Filename=FILENAME,
        Key='files/'+FILENAME)
    
# final report generator
def create_analytics_report(NAME, AGE, SEX, CUST_HEIGHT, WEIGHT, LIFESTYLE, FOOD, GOAL, CUST_HEIGHT_FT, BMR, BMI, IDEAL_WEIGHT, CLASS, CALORIES, PROTEIN, CARBS, FATS, FIBER):
    HEIGHT = 297
    WIDTH = 210
    
    pdf = FPDF(orientation = 'L', unit = 'mm', format=(HEIGHT, WIDTH))

    pdf.add_page()
    coverPage(pdf, WIDTH, HEIGHT, NAME, AGE, SEX, CUST_HEIGHT, WEIGHT, LIFESTYLE, FOOD, GOAL, CUST_HEIGHT_FT, BMR, BMI, IDEAL_WEIGHT, CLASS, CALORIES, PROTEIN, CARBS, FATS, FIBER)
    
    name = str(round(time.time())) + '_' + NAME +'.pdf'
    FILESTR = pdf.output(name=name, dest = 'F')
    return store_file(FILENAME=name, FILESTR=FILESTR)

def report(NAME, AGE, SEX, CUST_HEIGHT, WEIGHT, LIFESTYLE, FOOD, GOAL, GOAL2):
#def report(NAME, AGE, SEX):

    BMR = BMRCalculator(WEIGHT, CUST_HEIGHT, SEX, AGE)
    CUST_HEIGHT_FT = heightConverter(CUST_HEIGHT)
    BMI, CLASS, IDEAL_WEIGHT = BMIidealWeightCalculator(WEIGHT, CUST_HEIGHT, SEX)
    MAINTENANCE_CALORIE = MaintenanceCalorieCalculator(BMR, LIFESTYLE)
    CALORIES = ActualCaloriePlan(MAINTENANCE_CALORIE, GOAL, GOAL2)
    CARBS, PROTEIN, FATS, FIBER = MacroCalculator(MAINTENANCE_CALORIE, CALORIES)

    if MAINTENANCE_CALORIE < 1500:
        text = {
            "Name":NAME,
            "Age": AGE,
            "Message": "Your Weight Loss goal is too aggressive, please reconsider your goals",
        }
    
    else:
        text = {
            "Name":NAME,
            "Message": "Success, Your customized report is ready, please proceed with payment to download it",
        }
        create_analytics_report(NAME, AGE, SEX, CUST_HEIGHT, WEIGHT, LIFESTYLE, FOOD, GOAL, CUST_HEIGHT_FT, BMR, BMI, IDEAL_WEIGHT, CLASS, CALORIES, PROTEIN, CARBS, FATS, FIBER)
    
    return text

#report(NAME, AGE, SEX, CUST_HEIGHT, WEIGHT, LIFESTYLE, FOOD, GOAL, GOAL2)
