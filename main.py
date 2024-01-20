import re
import json
import random
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class auto_searching():
        def __init__(self) -> None:
            self.options = webdriver.ChromeOptions()
            self.service = Service('chromium/chromedriver.exe')
            self.service.creation_flags = CREATE_NO_WINDOW
            self.options.add_argument("--log-level=3")
            self.options.add_experimental_option("detach", True) #keep open
            self.options.binary_location = 'chromium/chrome.exe'
            self.driver = webdriver.Chrome(service=self.service, options=self.options)
            self.actions = ActionChains(self.driver)
            # self.tag_names = ["Thương mại Thành Thái", "Tập đoàn Thành Thái"]
            self.webpage_content = None
            self.result_list = []
            self.href_list = []
            self.correct_link = []
            self.missing_link = []
            self.check_link = []
            self.num = 1
            self.num_link = 0
            self.wait_Time = 5
            self.check = True
            self.xpath_database = {
                                    "Find_Box" :[
                                        "/html/body/div[",
                                        "]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea"],
                                    "Next_Page_Button":"//*[@id='pnnext']/span[2]",
                                    "Down_Page_Button":"//*[@id='botstuff']/div/div[3]/div[4]/a[1]/h3/div",
                                    "Check_Block_Find":"//*[@id='ofr']/i/a",
                                    "Erro_catching":"/html/body/div[6]/div/div[9]/div/div[1]/div/div/div[1]/div"
                                }
        # Mở trình duyẹt tìm kiếm
        def Open_browser (self):
            self.driver.get("http://google.com")
            

        def v_try(self, data, key):
            div_number = 0
            while True:
                condition = self.xpath_database[data][0] + str(div_number) + self.xpath_database[data][1]

                try: 
                    if key != None: self.driver.find_element(by = By.XPATH, value = condition).send_keys(key)
                    if key == "delete1": self.driver.find_element(by = By.XPATH, value = condition).send_keys(Keys.CONTROL, "a", Keys.DELETE)
                    if key == "get_text": return (self.driver.find_element(by = By.XPATH, value = condition).get_attribute("innerHTML"), condition)
                    if key == "json":
                        json = self.driver.find_element(by = By.XPATH, value = condition)
                        self.driver.execute_script("arguments[0].click();", json)
                    else: self.driver.find_element(by = By.XPATH, value = condition).click()

                    if not key == "get_text": return condition
                    break

                except: div_number += 1
            sleep(2)

        # Tạo ra nhiều tab để làm việc với từng từ khóa
        # def Creat_Tab(self,tab):
        #     for i in range (1,tab):
        #         try:self.driver.execute_script("window.open();")
        #         except:print("lỗi")

        # Nhập tên công ty muốn tìm vào thanh tìm kiếm
        def Find_company(self,name_company):
            click = self.v_try(data = "Find_Box", key = None)
            self.driver.find_element(by = By.XPATH, value =click).send_keys(name_company)
            self.driver.find_element(by = By.XPATH, value =click).send_keys(Keys.ENTER)

        # tự động tìm một thành phần cuối trang web, nếu không có tiếp tục nhấn pagedowwn để kéo xuống
        def Page_down(self):
            num = 0
            while True:
                try:
                    #trường hợp google hiện các tìm kiếm theo từng trang
                    self.driver.find_element(by = By.XPATH, value =self.xpath_database["Next_Page_Button"])
                    self.check = True
                    break
                except:
                    if num >3:
                        try:
                            # trường hợp google hiện các tìm kiếm trong 1 trang duy nhẩt và phải kéo xuống dưới để hiện thêm kết quả tìm kiếm.
                            self.driver.find_element(by = By.XPATH, value =self.xpath_database["Down_Page_Button"])
                            self.check = False
                            break
                        except: self.driver.find_element(by = By.XPATH, value ='html').send_keys(Keys.PAGE_DOWN)
                    else:
                        try:
                            # Đợi tối đa 3 giây cho phần tử hiển thị
                            wait = WebDriverWait(self.driver, self.wait_Time)
                            element = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath_database["Check_Block_Find"])))
                            print("Tìm thấy Check_Block_Find")
                            break
                        except TimeoutException:
                            self.driver.find_element(by = By.XPATH, value ='html').send_keys(Keys.PAGE_DOWN)
                            num +=1
                            sleep(0.5)
            return self.check 

        # lấy code của trang web về
        def Webpage_content(self):     
            self.webpage_content = self.driver.page_source
            return self.webpage_content

        # Tìm và lọc ra các thẻ div chứa các thẻ h3 chứa tên của công ty
        # def Find_link(self):
        #     soup = BeautifulSoup(self.webpage_content, 'html.parser')
        #     result_divs = set()
        #     for tag_name in self.tag_names:
        #         target_h3_tags = soup.find_all("h3", string=re.compile(tag_name, re.IGNORECASE))
        #         for h3_element in target_h3_tags:
        #             div_parent = h3_element.find_parent("div")
        #             if div_parent:
        #                 result_divs.add(div_parent)

        #     for h3_element in result_divs:
        #         self.result_list.append(str(h3_element))

        #     return self.result_list

        # Tìm và lọc các thẻ div chứa các thẻ h3.
        def Find_link(self):
            soup = BeautifulSoup(self.webpage_content, 'html.parser')
            result_divs = set()
            target_h3_tags = soup.find_all("h3")

            for h3_element in target_h3_tags:
                div_parent = h3_element.find_parent("div")               if div_parent:
                    result_divs.add(div_parent)

            for h3_element in result_divs:
                self.result_list.append(str(h3_element))

            return self.result_list

        # Lấy link từ các thẻ div đã lọc ở find_link
        def Get_link(self):
            for div_tag in self.result_list:
                soup = BeautifulSoup(div_tag, 'html.parser')
                a_tag = soup.find("a")
                if a_tag:
                    # Lấy giá trị của thuộc tính href
                    href_value = a_tag.get('href', None)
                    href_value = str(href_value)
                    self.href_list.append(href_value) 
            print(self.href_list)
            return self.href_list

        # Kiểm tra xem các link đã lọc có nằm trong list link cho trước. Nếu có thì thêm vào list(correct_link)
        def Correct_link(self,links):
            for link in self.href_list:
                if link not in self.check_link:
                    if self.missing_link == []:
                        if link in links:
                            self.correct_link.append(link)
                    elif self.missing_link != []:
                        if link in self.missing_link:
                            self.correct_link.append(link)
            return self.correct_link

        # Các link ở trong link cho trước không tồn tại trong correct_link thì sẽ đưa vào missing_link để lưu trữ
        def Defind_missing_link(self,links):
            for link in links:
                if link not in self.correct_link:
                    self.missing_link.append(link)
                elif link in self.correct_link:
                    if link in self.missing_link:
                        self.missing_link.remove(link)
            return self.missing_link

        # Truy cập vào các link đã được lấy ở Correct_link, đồng thời quay ngược lại trang tìm kiếm sau 1 khoảng thời gian ở lại trong trang
        def Go_to_link(self):
            print(self.correct_link)
            if self.correct_link !=[]:
                for link in self.correct_link:
                    self.check_link.append(link)
                    self.num_link += 1
                    try:
                        print(link)
                        self.driver.execute_script(f"window.open('{link}', '_blank');")
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        # self.driver.back()
                        sleep(1)
                        try :self.driver.execute_script("location.reload();")
                        except: print("Không load được")
                        sleep(1)

                    except Exception as e:
                        print(f"Không thể click vào thẻ h3: {link} - Lỗi: {e}")
            else:
                print("Không tìm thấy thẻ h3 phù hợp với biểu thức chính quy tag_pattern")
                return False

            try :self.driver.find_element(by = By.XPATH, value ="body").send_keys(Keys.F5)
            except: None
            return self.num_link
        def Roll_Page(self,stoptime):
            print(self.num_link)
            for i in range (0,self.num_link):
                tab = i+1
                self.driver.switch_to.window(self.driver.window_handles[tab])
                times = stoptime / 100
                limited_time=0
                while True:
                    if limited_time >= stoptime:
                        break
                    else:
                        limited_time += times
                        self.driver.execute_script("window.scrollBy(0, 100);")
                        sleep(times)
                random_link_script = """
                var linkElements = document.getElementsByTagName('a');
                var randomIndex = Math.floor(Math.random() * linkElements.length);
                return linkElements[randomIndex];
                """
                random_link = self.driver.execute_script(random_link_script)
                print(random_link)

                # Nhấp vào liên kết ngẫu nhiên bằng JavaScript
                self.driver.execute_script("arguments[0].click();", random_link)
                sleep(5)

        def Next_page(self):
            print("Start")
            # input()
            # self.v_try(data = "Next_Page_Button", key = None)
            if self.check == True:
                self.driver.find_element(by = By.XPATH, value =self.xpath_database["Next_Page_Button"]).click()
                print("lần ",self.num)
                sleep(5)

                try:
                    #Erro catching:dòng chữ đầu ngay dưới thanh tìm kiếm: Trang 4 trong khoảng 14.200.000 kết quả (0,40 giây) 
                    self.driver.find_element(by = By.XPATH, value =self.xpath_database["Erro_catching"]) 
                    self.driver.execute_script("location.reload();")
                except:
                    self.driver.execute_script("location.reload();")

            else:
                self.driver.find_element(by = By.XPATH, value =self.xpath_database["Down_Page_Button"]).click()
                print("lần ",self.num)
                sleep(3)

            self.webpage_content = None
            self.result_list = []
            self.href_list = []
            self.correct_link = []
            print("reset list")            
            self.num +=1
            print("success")
            sleep(1)

        def Check_Block_Find(self,page):
            check = False
            while True:
                self.Page_down()
                if self.check == True:
                    try:
                        self.driver.find_element(by = By.XPATH, value =self.xpath_database["Check_Block_Find"]).click()
                        check = True
                        self.num = 1
                    except:
                        print("Chưa thành công ")
                        if self.num > page:
                            for i in range (1,self.num):
                                self.driver.back()
                            break
                        else:self.Next_page()
                else:
                    try:
                        self.driver.find_element(by = By.XPATH, value =self.xpath_database["Check_Block_Find"]).click()
                        check = True
                        self.num = 1
                        break
                    except:
                        print("Chưa thành công ")

                        if self.num > page:break
                        else:self.Next_page()
                if check == True:
                    break
                sleep(1)
            return self.num


        def Quit(self):
            self.driver.quit()

        # Mở nhiều tab sau đó trên mỗi tab sẽ lmaf việc 1 với thứ tự từ tab đầu đến tab cuối cùng
        # def Launching(self,keyword:str,link:list,time:int,keywordtime:int,page:int,tab:int):
        #     for i in range (0,tab):
        #         numpage = i
        #         self.driver.switch_to.window(self.driver.window_handles[i])
        #         self.driver.get("http://google.com")
        #         self.Find_company(keyword)
        #         print("company")

        #         for y in range(0,page):
        #             #Kéo xuống cuối trang
        #             self.Page_down()
        #             print("page down")
        #             #Lấy html của trang web về
        #             self.Webpage_content()
        #             print("load web")
        #             #Lọc ra các thẻ div chứa link
        #             self.Find_link()
        #             print("find link")
        #             #Lọc ra các link
        #             self.Get_link()
        #             print('get link')
        #             #Lọc ra các link nằm trong List cho trước
        #             self.Correct_link(link)
        #             print("correct link")
        #             #Lọc các link không tìm thấy trong List đã cung cấp
        #             self.Defind_missing_link(link)
        #             print("missing link")
        #             #Truy cập vào đường link
        #             self.Go_to_link(time,numpage)
        #             print("Go to link")

        #             #Nhấn qua trang kế tiếp
        #             if page > 1:
        #                 self.Next_page()
        #                 print("next page")
        #             sleep(keywordtime)
        #             print(keywordtime)      
        #         self.num = 1     


link=["https://sualaptopvinhphat.com/gia-thay-ban-le-laptop-va-sua-ban-le-may-tinh-bao-nhieu/",'https://sualaptopvinhphat.com/gia-sua-ban-le-laptop-hien-nay-la-bao-nhieu/','https://vinhphatstore.vn/cach-sua-ban-le-laptop-tai-nha-don-gian/']
time= 5# Go to link
name_company = "bản lề laptop"# Find name
page = 10
keywordtime = 10
a =auto_searching()
def run_task (a, keyword:str,link:list,time:int,keywordtime:int,page:int) -> None:
    #Mở browser
    a.Open_browser()
    print("open")
    # a.Creat_Tab(tab)
    # a.Launching(name_company,link,time,keywordtime,page,tab)

    #Nhập và tìm tên công ty
    a.Find_company(keyword)
    print("company")
    if page > 1:
        print("check block")
        a.Check_Block_Find(page)
    for i in range(0,page):
        #Kéo xuống cuối trang
        a.Page_down()
        print("page down")
        #Lấy html của trang web về
        a.Webpage_content()
        print("load web")
        #Lọc ra các thẻ div chứa link
        a.Find_link()
        print("find link")
        #Lọc ra các link
        a.Get_link()
        print('get link')
        #Lọc ra các link nằm trong List cho trước
        a.Correct_link(link)
        print("correct link")
        #Lọc các link không tìm thấy trong List đã cung cấp
        a.Defind_missing_link(link)
        print("missing link")
        #Truy cập vào đường link
        print("Go to link")
        a.Go_to_link()
        #Nhấn qua trang kế tiếp
        if page > 1:
            a.Next_page()
            print("next page")
    a.Roll_Page(time)
    sleep(keywordtime)
    print(keywordtime)
run_task(a,name_company,link,time,keywordtime,page)

