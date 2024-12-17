from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os
import re
import numpy as np
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

# Location using the provided XPath
try:
    location = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[3]/div/span[1]'))).text
except:
     print("Location not found with method 1")
     try: 
        location = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[3]/div/span[1]'))).text
     except:
         location = 'Location not found'
# Date Posted (will be today’s date)
date_applied = datetime.today().strftime('%#m/%d/%Y')

#Salary
try:
    salary = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[1]'))).text
except:
    salary = ""  # Leave blank if salary is not found


# Seniority detection based on the job title
seniority = "Mid"  # Default to Mid
if any(keyword.lower() in job_title.lower() for keyword in ['senior', ' ii ', ' 2 ', 'iii', 'iiii', ' 3 ', ' 4 ', ' 5 ']):
    seniority = "Senior"

# Category detection based on keywords in the job title
categories = ['Data Analytics', 'Data Science', 'Data Engineering', 'Business Intelligence']
category = 'Data Engineering'  # Default category

# Check the job title for any of the categories
for cat in categories:
    if cat.lower() in job_title.lower():
        category = cat
        break  # Stop at the first match

# Print the results
print(f"\nJob Title: {job_title}")
print(f"Company Name: {company_name}")
print(f"Location: {location}")
print(f"Date Applied: {date_applied}")
print(f"\nSalary: {salary}")
print(f"Seniority: {seniority}")
print(f"Category: {category}")


#%% File appending

# Append the data to an Excel file Put your cureent
file_name = "Job Tracker.xlsx"
new_data = pd.DataFrame({
    'Title': [job_title],
    'Company': [company_name],
    'Location': [location],
    'Date': [date_applied],  # Using today's date
    'Salary': [salary],
    'Seniority': [seniority],
    'Category': [category]# Will be blank if not found
})


# Check if the file exists, if it does append data, otherwise create a new one
if os.path.exists(file_name):
    existing_data = pd.read_excel(file_name)
    updated_data = pd.concat([existing_data, new_data], ignore_index=True)
else:
    updated_data = new_data

#%% Updataed data transformations

# Function to clean and convert shorthand salary
def convert_salary(salary):
    
    # Check if salary is NaN or not a string
    if pd.isna(salary) or not isinstance(salary, str):
        return np.nan, np.nan
    # Check if the salary is a range
    if '-' in salary:
        # Split the salary into min and max parts
        min_salary, max_salary = salary.split('-')
    else:
        # If it's a single salary, treat it as both min and max
        min_salary = max_salary = salary

    # Remove 'k' and convert to numeric only if 'k' is present
    if 'k' in min_salary.lower():
        min_salary = int(re.sub(r'[^\d]', '', min_salary)) * 1000
    else:
        min_salary = int(re.sub(r'[^\d]', '', min_salary))
    
    if 'k' in max_salary.lower():
        max_salary = int(re.sub(r'[^\d]', '', max_salary)) * 1000
    else:
        max_salary = int(re.sub(r'[^\d]', '', max_salary))
    
    return min_salary, max_salary

try:
    # Apply the function to the Salary column
    updated_data['Min Salary'], updated_data['Max Salary'] = zip(*updated_data['Salary'].apply(convert_salary))  
except:
    print("Salary not found")
    updated_data['Min Salary'] = ""
    updated_data['Max Salary'] = ""
    pass
#drop old column
updated_data = updated_data.drop(columns=['Salary'])

# Rearrange columns to place 'Min Salary' and 'Max Salary' where 'Salary' was
updated_data = updated_data[['Date', 'Category', 'Title', 'Seniority', 'Company', 'Min Salary', 'Max Salary', 'Location']]
 
#convert df date to right format
updated_data['Date'] = pd.to_datetime(updated_data['Date']).dt.strftime('%#m/%d/%Y') 



# Save the updated data to the Excel file
updated_data.to_excel(file_name, index=False)


# Close the driver
driver.quit()

print(f"\n{job_title} at {company_name} successfully appended to {file_name}")

# Close the driver
driver.quit()
