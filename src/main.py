# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 09:14:06 2024

@author: Matth
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os
from datetime import datetime
# Set up the Chrome driver using webdriver_manager for automatic driver management


#%% setup
url = input("Enter Linkedin Job URL:\n")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
#%% Logging in

# LinkedIn credentials to auto sign in
linkedin_username = ""  # Replace with your LinkedIn email
linkedin_password = "" 
# Define explicit waits
wait = WebDriverWait(driver, 10)
# Open LinkedIn login page
driver.get("https://www.linkedin.com/login")

# Allow the page to load
time.sleep(3)

# Enter username
driver.find_element(By.ID, 'username').send_keys(linkedin_username)

# Enter password
driver.find_element(By.ID, 'password').send_keys(linkedin_password)

# Click the "Sign in" button
driver.find_element(By.XPATH, '//button[@type="submit"]').click()

# Allow time for login
time.sleep(5)  # Adjust based on your internet speed


#%% job search

# Open LinkedIn job page
driver.get(url)
# Allow the page to load
driver.implicitly_wait(5)


# Extract job details using Selenium
try:
    job_title = driver.find_element(By.CSS_SELECTOR, 'h1').text
except:
    job_title = "Job title not found"

#compnay name
try:
    company_name = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[1]/div[1]/div/a'))).text
except:
    company_name = "Company name not found"

# Location
try:
    location = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[3]/div/span[1]'))).text
except:
    location = "Location not found"

# Date Posted (will be today’s date)
date_applied = datetime.today().strftime('%-m/%d/%y')

# Salary 

try:
    salary = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[7]/div[1]/div/div[2]/p'))).text
except:
    salary = ""  # Leave blank if salary is not found




# Print the results
print(f"\nJob Title: {job_title}")
print(f"Company Name: {company_name}")
print(f"Location: {location}")
print(f"Date Applied: {date_applied}")
print(f"Salary: {salary}")



#%% File appending

# Append the data to an Excel file Put your cureent
file_name = r"C:\Users\Matth\OneDrive\Documents\JobMaxing\Job Tracker.xlsx"
new_data = pd.DataFrame({
    'Title': [job_title],
    'Company': [company_name],
    'Location': [location],
    'Date': [date_applied],  # Using today's date
    'Salary': [salary]  # Will be blank if not found
})

# Check if the file exists, if it does append data, otherwise create a new one
if os.path.exists(file_name):
    existing_data = pd.read_excel(file_name)
    updated_data = pd.concat([existing_data, new_data], ignore_index=True)
else:
    updated_data = new_data


# Save the updated data to the Excel file
updated_data.to_excel(file_name, index=False)

print(f"\nData successfully appended to {file_name}")

# Close the driver
driver.quit()

print(f"\n{job_title} at {company_name} successfully appended to {file_name}")

# Close the driver
driver.quit()
