import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


website_to_check = 'https://www.nba.com/stats/players/traditional?PerMode=Totals&sort=PTS&dir=-1'

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
driver.get(website_to_check)

try:
    # Close the cookie acceptance form, if it appears
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-close-btn-container"]/button'))
    ).click()
except Exception as e:
    print('No cookie acceptance form found')


# Wait for the table header to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "Block_blockContent__6iJ_n"))
)
# Extract column headers
columns = driver.find_elements(By.CSS_SELECTOR, 'table thead tr th')[14:44]
heading_list = [item.text for item in columns]
with open('results.csv',mode='w') as file:
    writer=csv.writer(file)
    writer.writerow(heading_list)

print("Number of columns:", len(columns))
# Initialize table data list
for i in range(9):
    print(f"Scraping page {i + 1}...")
    # Wait for the data rows to be present and extract data
    data = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table tbody tr'))
    )

    for item in data[10:]:
        with open('results.csv', mode='a') as file:
            text = item.text
            new_text= text.replace(' ',',')
            file.write(f'{new_text}\n')
    # Attempt to click the pagination "Next" button, if not on the last page
    if i < 8:
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]'))
            )
            next_button.click()
        except Exception as e:
            print("Next button not clickable:", e)
            break
