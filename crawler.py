from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Selenium WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)

# URL
url = 'https://supportgowhere.life.gov.sg/schemes'

# Open the URL
driver.get(url)
time.sleep(5)  # Wait for the JavaScript to load the content

# Extract the scheme information
schemes = []
sections = driver.find_elements(By.CLASS_NAME, 'MainSection-sc-k5l9t0-2.kogops')

for section in sections:
    title = section.find_element(By.CLASS_NAME, 'Title-sc-k5l9t0-6.hNPwaO').text.strip()
    description = section.find_element(By.CLASS_NAME, 'StyledSpan-sc-dswz5v-0.gwUYba.Description-sc-k5l9t0-7.lktKRv').text.strip()
    tags = [tag.text for tag in section.find_elements(By.CLASS_NAME, 'Tag-sc-k5l9t0-10.hiZaSn')]
    schemes.append({
        'Title': title,
        'Description': description,
        'Tags': ', '.join(tags)
    })

# Convert the list of dictionaries to a pandas DataFrame
schemes_df = pd.DataFrame(schemes)

# Save the DataFrame to a CSV file
schemes_df.to_csv('schemes_data.csv', index=False)

print(schemes_df)

driver.quit()
