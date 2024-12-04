import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Set up the ChromeDriver service

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

page_url = "https://www.amazon.eg/-/en/"
driver.get(page_url)

# # Wait for search results to appear and click the desired link
# WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT,"Search")))
time.sleep(10)

# Locate the search bar, type the search item
search_bar = driver.find_element(By.XPATH,"//input[@id = 'twotabsearchtextbox']")
search_bar.send_keys("laptop lenovo")
search_bar.send_keys(Keys.ENTER)


items =[]
for i in range(1):
    # Start scraping items from page
    # class="a-size-base-plus a-color-base a-text-normal"
    # <span class="a-size-base-plus a-color-base a-text-normal">IdeaPad Gaming 3 15IAH7 Laptop - 12th Intel Core i7-12650H 10-Cores, 16GB RAM, 512GB SSD, NVIDIA GeForce RTX 3060 6GB GDDR6 Graphics, 15.6" FHD (1920x1080) IPS 165Hz, Backlit, Dos - Onyx Grey</span>
    item_title = driver.find_elements(By.XPATH ,"//span[@class='a-size-base-plus a-color-base a-text-normal']")

    #<span class="a-price-whole">45,999<span class="a-price-decimal">.</span></span>
    item_price = driver.find_elements(By.XPATH ,"//span[@class='a-price-whole']")
    for title,price in zip(item_title,item_price):
        try:
            print("title: ",title.text)
            print("price: ",price.text)
            print()
            items.append([title.text,price.text])
        except Exception as e:
            print("error: ", e)

        #go to next page

    try:
        next_bottom = driver.find_element(By.XPATH,"//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator']")
        next_bottom.click()
    except Exception as e:
        print("error:no more pages ")
   

#create data frame to save data
# Create a DataFrame from the scraped data
data = pd.DataFrame(data=items, columns=["mobile_name", "price"])

# Save the data to a CSV file
data.to_csv("amazon_laptop_lenovo.csv", index=False)

driver.close()
#pause
time.sleep(3)
driver.quit()