import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

cred = credentials.Certificate("auto_clicking.json")
firebase_admin.initialize_app(cred)

#Tạo tk
def create_user(email):
	try:
		user = auth.create_user(email=email,password="000000")
		return user
	except:
		return None

password = "ducdeptrai"
password = password + "@gmail.com"
email = "ducluyen1609@gmail.com"
create_user(email)
if create_user:
	print("tạo Tài khoản thành công!")
else:
	print("tạo Tài khoản thất bại!")

# #Cập nhật TK
# def update_user(email,password):
# 	try:
# 		user = auth.update_user(uid=email,email=password,password="000000")
# 		return user
# 	except:
# 		return None

# password = "deptrai"
# password = password + "@gmail.com"
# email = "ducluyen1609@gmail.com"
# update_user(email,password)

# if update_user:
# 	print("Cài lại mật khẩu Tài khoản thành công!")
# else:
# 	print("Cài lại mật khẩu Tài khoản thất bại!")

# #Đăng nhập Tk
# def login_user(user_email, user_password):
#     user = auth.get_user(uid=user_email)
#     password = user.email
#     if password !=  user_password:
#     	print("đăng nhập thất bại")
#     else: print("Đăng nhập thành công {0}".format(password))

# email = "ducluyen1609@gmail.com"
# password = "deptrai"
# password = password + "@gmail.com"
# logged_in_user = login_user(email, password)





# import threading
# import re
# import json
# from time import sleep
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from subprocess import CREATE_NO_WINDOW
# from selenium.webdriver.common.by import By
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service



# def run_tab(url):
# 	options = webdriver.ChromeOptions()
# 	service = Service('chromium/chromedriver.exe')
# 	service.creation_flags = CREATE_NO_WINDOW
# 	options.add_argument("--log-level=3")
# 	options.add_experimental_option("detach", True) #keep open
# 	options.binary_location = 'chromium/chrome.exe'
# 	driver = webdriver.Chrome(service=service, options=options)
# 	driver.get(url)
# 	sleep(1)

# youtube_url = "https://www.youtube.com"

# threads = []
# for i in range (0,2):
# 	youtube_thread = threading.Thread(target=run_tab, args=(youtube_url,))
# 	threads.append(youtube_thread)

# for thread in threads:
#     thread.start()

# for thread in threads:
#     thread.join()

# print("Tất cả các tác vụ đã hoàn thành.")
