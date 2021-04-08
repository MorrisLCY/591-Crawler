from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time, datetime
from bs4 import BeautifulSoup
import pandas as pd
from pyvirtualdisplay import Display
# pyvirtuladisplay ubuntu only
# 華文專業鋼鐵網 H型鋼

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
driver.get("https://www.steelnet.com.tw/index.php?action=market_taiwan&amp;week_country_id=1")
time.sleep(2)

# find element than key in account
username = driver.find_element_by_name('account')
username.send_keys("bestw")
time.sleep(2)

# find element than key in ps
password = driver.find_element_by_name("password")
password.send_keys("hb08787")
time.sleep(2)

# find and click to log in
login_btn = driver.find_element_by_css_selector(".login-btn")
login_btn.click()


# 檢查是否有彈出視窗 並接受
try:
    WebDriverWait(driver, 3).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
except TimeoutException:
    print("no alert")
time.sleep(5)


# choose 行情表查詢
table_btn = driver.find_element_by_name("query_type")
table_btn.click()
select_table = driver.find_element_by_xpath("//option[@value='table']")
select_table.click()

x = datetime.datetime.now()
year = x.strftime("%Y")
month = x.strftime("%m")
week = str((x.day-1)//7+1)

# x = datetime.datetime.now()
# y = datetime.datetime(2020, 1, 15)
# print(y.strftime("%m"))
# print((y.day-1)//7+1)

# choose  start year and month
year_btn = driver.find_element_by_name("chart_line_year_start")
year_btn.click()
select_year = Select(driver.find_element_by_name("chart_line_year_start"))
select_year.select_by_value("2019")

month_btn = driver.find_element_by_name("chart_line_month_start")
month_btn.click()
select_month = Select(driver.find_element_by_name("chart_line_month_start"))
select_month.select_by_value("1")

# choose  end year and month
year_btn = driver.find_element_by_name("chart_line_year_end")
year_btn.click()
select_year = Select(driver.find_element_by_name("chart_line_year_end"))
select_year.select_by_value(year)

month_btn = driver.find_element_by_name("chart_line_month_end")
month_btn.click()
select_month = Select(driver.find_element_by_name("chart_line_month_end"))
select_month.select_by_value(month)

# choose 普通鋼材
o_iron = driver.find_element_by_name("chart_line_category_1")
o_iron.click()
original_iron = Select(driver.find_element_by_name("chart_line_category_1"))
original_iron.select_by_value("普通鋼材")

# choose 型鋼
t_iron = driver.find_element_by_name("chart_line_category_2")
t_iron.click()
iron_two = Select(driver.find_element_by_name("chart_line_category_2"))
iron_two.select_by_value("型鋼")

# choose H型鋼
multi_select = driver.find_element_by_id("distinct_id_block")
multi_select.click()
select_one = driver.find_element_by_id("distinct_id_0")
select_one.click()

# 確認查詢
search_btn = driver.find_element_by_id("btnQuery")
search_btn.click()
time.sleep(5)

# 跳出iframe 友善列印
print_frame = driver.find_element_by_xpath("//iframe")
driver.switch_to.frame(print_frame)
time.sleep(2)

driver.find_elements_by_class_name("table table-bordered")
soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.close()
# print(soup.prettify())
# -------------------------- ETL
date_table = soup.find_all(attrs={"data-title": "日期"})
high_price = soup.find_all(attrs={"data-title": "最高價"})
price_limit = soup.find_all(attrs={"data-title": "漲跌幅"})
down_price = soup.find_all(attrs={"data-title": "最低價"})

date_list = []
h_price = []
price_l = []
d_price = []
for i in date_table:
    date_list.append(i.string)
for i in high_price:
    h_price.append(i.string)
for i in price_limit:
    price_l.append(i.string)
for i in down_price:
    d_price.append(i.string)

iron_dict = {"日期": date_list,
             "最高價": h_price,
             "最低價": d_price}
iron_df = pd.DataFrame(iron_dict)

rows = len(iron_df)
limit_h = []
limit_l = []
for i in range(0, rows*2, 2):
    limit_h.append(price_l[i])
for j in range(1, rows*2, 2):
    limit_l.append(price_l[j])

iron_df.insert(2, "高價漲跌幅", limit_h)
iron_df.insert(4, "低價漲跌幅", limit_l)

file_path = '/home/Iron_all/CrawlerResults/' + 'H_iron.csv'
iron_df.to_csv(file_path, encoding='big5')
