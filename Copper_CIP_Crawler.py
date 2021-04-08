from selenium import webdriver
from selenium.webdriver.support.ui import  Select
from selenium.webdriver.chrome.options import Options
import time, datetime
from bs4 import BeautifulSoup
import pandas as pd
from pyvirtualdisplay import Display
# pyvirtuladisplay ubuntu only

def back_to_default_to_tab_one():
    driver.switch_to.default_content()
    i_main = driver.find_element_by_id('iMain')
    driver.switch_to.frame(i_main)

    page_nine = driver.find_element_by_id('Pag9')
    driver.switch_to.frame(page_nine)

    tab_one = driver.find_element_by_name('Tab1')
    driver.switch_to.frame(tab_one)


def back_to_default_to_page_nine():
    driver.switch_to.default_content()

    i_main = driver.find_element_by_id('iMain')
    driver.switch_to.frame(i_main)

    page_nine = driver.find_element_by_id('Pag9')
    driver.switch_to.frame(page_nine)

# CIP商品行情網

# Ubuntu setting
display = Display(visible=0, size=(1980, 1080))
display.start()

# chrome exe and driver setting
options = Options()

# options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
options.binary_location = "/usr/bin/google-chrome"
# webdriver_path = "C:/Users/Asus/PycharmProjects/Iron_crawler/chromedriver.exe"
webdriver_path = "/usr/local/bin/chromedriver"

driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
driver.maximize_window()
driver.get("http://cip.chinatimes.com/newindex.asp")
time.sleep(2)

# switch to frame ----------1 step Log in
frame_main = driver.find_element_by_id('iMain')
driver.switch_to.frame(frame_main)

frame_page = driver.find_element_by_id('Pag1')
driver.switch_to.frame(frame_page)

driver.find_element_by_id("Table5")
driver.find_element_by_id("Form1")

# find input account
account = driver.find_element_by_id("Text1")
account.clear()
account.send_keys('bestw')
time.sleep(2)

# find input psword
password = driver.find_element_by_id("Password1")
password.clear()
password.send_keys('hb08787')
time.sleep(2)

# find login btn and go
login_btn = driver.find_element_by_xpath("//input[@src='images/login.gif']")
login_btn.click()
time.sleep(5)

# -----------------2 step 國際商品行情

driver.find_element_by_id("Table2")
driver.find_element_by_id("el2")
link = driver.find_element_by_id("lnk2")
link.click()
time.sleep(5)

# ----------------3 step 金屬

back_to_default_to_tab_one()
cmd_frame = driver.find_element_by_id('cmdM')
driver.switch_to.frame(cmd_frame)

metal_link = driver.find_element_by_id('indB1')
metal_link.click()
time.sleep(5)

# -----------------4 step 物料-銅

back_to_default_to_tab_one()
spec_frame = driver.find_element_by_id('frameSpecM')
driver.switch_to.frame(spec_frame)

copper = driver.find_element_by_xpath("//input[@value='B109']")
copper.click()

# -----------------5 step 規格 銅倫敦 LME 現貨收盤價

back_to_default_to_tab_one()
specS_frame = driver.find_element_by_id('frameSpecS')
driver.switch_to.frame(specS_frame)

london_lme = driver.find_element_by_xpath("//input[@value='C2741005000003']")
london_lme.click()

back_to_default_to_tab_one()
search_btn = driver.find_element_by_xpath("//input[@value='查詢']")
search_btn.click()
time.sleep(5)

# -----------------6 step 開始進入日期選擇查詢框架
back_to_default_to_page_nine()
tab2_international = driver.find_element_by_name('Tab2_International')
driver.switch_to.frame(tab2_international)

# select month and week
x = datetime.datetime.now()
month = x.strftime("%m")
week = str((x.day-1)//7+1)

month_btn = Select(driver.find_element_by_id('EMM'))
month_btn.select_by_value(month)
time.sleep(1)

week_btn = Select(driver.find_element_by_id('EW'))
week_btn.select_by_value(week)
time.sleep(1)

# Search
week_price_search_btn = driver.find_element_by_id('cmdAverageQuery1')
week_price_search_btn.click()
time.sleep(5)


# -----------------7 step 週均價表格

back_to_default_to_page_nine()
tab3_international = driver.find_element_by_name('Tab3_International')
driver.switch_to.frame(tab3_international)

driver.find_element_by_id('tbList')
soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.close()
# -----------------8 step data ETL

# print(soup.prettify())
first_c = soup.find_all('td')
c_list = []
for i in first_c:
    c_list.append(i.string)

cooper_price = c_list[7:]

# append in every list
week_list = []
up_price = []
down_price = []

for i in range(3):
    for j in range(i, len(cooper_price), 3):
        if i == 0:
            week_list.append(cooper_price[j])
        elif i == 1:
            up_price.append(cooper_price[j])
        elif i == 2:
            down_price.append(cooper_price[j])

cooper_dict = {"日期": week_list,
               "上限均價": up_price,
               "下限均價": down_price}


file_path = '/home/Iron_all/CrawlerResults/' + 'copper_week_price.csv'
cooper_df = pd.DataFrame(cooper_dict)
cooper_df.to_csv(file_path, encoding='big5')

