import re
import json
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

# Khởi tạo trình duyệt
options = webdriver.ChromeOptions()
service = Service('chromium/chromedriver.exe')
service.creation_flags = CREATE_NO_WINDOW
options.add_argument("--log-level=3")
options.add_experimental_option("detach", True) #keep open
options.binary_location = 'chromium/chrome.exe'
driver = webdriver.Chrome(service=service, options=options)


# # Mở trang web
# driver.get("https://www.google.com")


# # Mở tab mới bằng cách gửi phím tắt Ctrl + T
# for i in range (1,10):
#     try:driver.execute_script("window.open();")
#     except:print("lỗi")

# # Mở một trang web khác trong tab mới
# # driver.get("https://www.google.com")

# # Chờ một chút để thấy sự chuyển đổi giữa các tab
# sleep(2)

# # Quay trở lại tab cũ bằng cách gửi phím tắt Ctrl + số thứ tự tab cũ (vd: Ctrl + 1 cho tab đầu tiên)
# for i in range (0,10):
#     driver.switch_to.window(driver.window_handles[i])
#     sleep(1)

# # Chờ một chút để thấy sự chuyển đổi giữa các tab
# input()

# # Đóng trình duyệt
# driver.quit()



# # Mở trang web
# driver.get("https://www.youtube.com")

# # Thực thi JavaScript để lấy danh sách tất cả các phần tử liên kết và chọn một phần tử ngẫu nhiên
# random_link_script = """
# var linkElements = document.getElementsByTagName('a');
# var randomIndex = Math.floor(Math.random() * linkElements.length);
# return linkElements[randomIndex];
# """
# random_link = driver.execute_script(random_link_script)
# print(random_link)

# # Nhấp vào liên kết ngẫu nhiên bằng JavaScript
# driver.execute_script("arguments[0].click();", random_link)
# new_tab_url = 'https://www.example.com'

# # Mở một trang web trong tab mới
# driver.execute_script(f"window.open('{new_tab_url}', '_blank');")

# input()
# # Đóng trình duyệt
# driver.quit()




driver.get("https://www.google.com/search?q=b%E1%BA%A3n+l%E1%BB%81+laptop&oq=b%E1%BA%A3n+l%E1%BB%81+laptop&aqs=chrome..69i57.984j0j7&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBBzk4NGowajeoAgCwAgA&sourceid=chrome&ie=UTF-8")
try:driver.find_element(by = By.XPATH, value = '//*[@id="ofr"]/i/a')
except:driver.find_element(by = By.XPATH, value ="//*[@id='pnnext']/span[2]").click()

a = driver.find_element(by = By.XPATH, value = '//*[@id="ofr"]/i/a').get_attribute("href")
print(a)
driver.get(a)