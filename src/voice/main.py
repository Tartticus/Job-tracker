import speech_recognition as sr
import pyfiglet
from time import sleep
import pandas as pd
from datetime import datetime
import os



# Identify Microphone
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Microphone {index}: {name}")



file_name = 'jobs.xlsx'


mic_index = 1  # Use the index for Microphone 1
recognizer = sr.Recognizer()

try:
    with sr.Microphone() as source:
        print("What is the name of the company?")
        audio = recognizer.listen(source) 
        
        print("Converting speech to text...")
        company = recognizer.recognize_google(audio)  
        print(f"You said: {company}")
        
        #company
        ascii_art = pyfiglet.figlet_format(company)
        print(ascii_art)
        
        
        
        #Position
        print("What is the position?")
        audio2 = recognizer.listen(source)  
        print("Converting speech to text...")
        position = recognizer.recognize_google(audio2)  
        print(f"You said: {position}")
        
        #Location
        print("What is the location?")
        audio3 = recognizer.listen(source)  
        print("Converting speech to text...")
        location = recognizer.recognize_google(audio3)  
        print(f"located at: {location}")
        
        
        
        
        
except sr.UnknownValueError:
    print("Sorry, could not understand the audio.")
except sr.RequestError:
    print("Error connecting to the recognition service.")



date_applied = datetime.today().strftime('%#m/%d/%Y')

new_data = pd.DataFrame({
    'Title': [position],
    'Company': [company],
    'Location': [location],
    'Date': [date_applied],  # Using today's date
  
})


# Check if the file exists, if it does append data, otherwise create a new one
if os.path.exists(file_name):
    existing_data = pd.read_excel(file_name)
    updated_data = pd.concat([existing_data, new_data], ignore_index=True)
else:
    updated_data = new_data
    
    
#convert df date to right format
updated_data['Date'] = pd.to_datetime(updated_data['Date']).dt.strftime('%#m/%d/%Y') 



# Save the updated data to the Excel file
updated_data.to_excel(file_name, index=False)
print(f"{position} at {company} saved at {file_name}")    
