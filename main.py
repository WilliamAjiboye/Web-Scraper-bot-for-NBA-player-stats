import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

website_to_check = 'https://www.nba.com/stats/players/traditional?PerMode=Totals&sort=PTS&dir=-1'

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
driver.get(website_to_check)
time.sleep(5)
# driver.quit()

try:
    driver.find_element(By.XPATH, '//*[@id="onetrust-close-btn-container"]/button').click()
except Exception as e:
    print('no cookie acceptance form')

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "Block_blockContent__6iJ_n"))
)

columns = driver.find_elements(By.CSS_SELECTOR, 'table thead tr th')[15:44]
heading_list = [items.text for items in columns]
print(len(columns))

table = []

for i in range(8):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Block_blockContent__6iJ_n"))
        )
    except Exception as e:
        print("Element not found:", e)
    else:
        time.sleep(3)
        data = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')[10:]
        for items in data:
            table.append(items)

        time.sleep(5)
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]'))
            )
            button.click()
        except Exception as e:
            print("Element not clickable:", e)
        time.sleep(4)


print(len(table))
print(table)