from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_top_mkt_cap():

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Navigate to the desired URL
    url = 'https://finviz.com/screener.ashx?v=111&o=-marketcap'
    driver.get(url)

    # # element = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[4]/table/tbody/tr/td/div/table[2]/tbody/tr[7]/td/table/tbody/tr/td[1]/div/table/tbody')

    element = driver.find_element(By.CSS_SELECTOR,'#screener-table')
    content=element.text
    # Print the extracted content
    print(content)
    driver.quit()

    content_list = content.split('\n')
    content_title_list = content_list[2::11]

    return content_title_list
