from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_stock_list(filter_):

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Navigate to the desired URL
    
    if filter_=="Mkt Cap":
        url = 'https://finviz.com/screener.ashx?v=111&o=-marketcap'
    elif filter_=="Uptrend":
        url= 'https://finviz.com/screener.ashx?v=111&f=ta_sma200_sb50,ta_sma50_pa&ft=3&o=-marketcap'
    driver.get(url)

    # # element = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[4]/table/tbody/tr/td/div/table[2]/tbody/tr[7]/td/table/tbody/tr/td[1]/div/table/tbody')

    element = driver.find_element(By.CSS_SELECTOR,'#screener-table')
    content=element.text
    # Print the extracted content
    driver.quit()

    content_list = content.split('\n')
    content_title_list = content_list[2::11]

    return content_title_list


