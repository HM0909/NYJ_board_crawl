from unicodedata import category
import re
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import urllib.request as ur
import time
from selenium.webdriver.common.alert import Alert
from db_manager import DatabaseManager
from webdriver_manager.chrome import ChromeDriverManager    # Mac

HEADER = ['제목', '조회수', 'URL', '첨부파일 URL', '작성자', '내용', '등록일']
ARGV_COUNT = 2
DATABASE_ID = "local"

# 남양주시립박물관(nyj)

base_url = "https://www.nyj.go.kr/museum/4606"
board_url = "https://www.nyj.go.kr/museum/4572" 
login_url = "https://www.nyj.go.kr/main/63?referer=https%3A%2F%2Fwww.nyj.go.kr%2Fmuseum%2F4606" 

driver = webdriver.Chrome(executable_path='C:\hm_py\chromedriver')    # Windows


def login():
    driver.get(base_url)

    # 로그인 페이지 이동
    element = driver.find_element_by_xpath('//*[@id="process_login"]')  
    driver.execute_script("arguments[0].click();", element)
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])  #새로 연 탭으로 이동
                  
    # 로그인
    user_id = ""
    password = ""

    driver.find_element_by_id('user_id').send_keys(user_id)
    time.sleep(5)
    driver.find_element_by_id('user_password').send_keys(password)
    time.sleep(5)
    element = driver.find_element_by_xpath('//*[@id="memberForm"]/fieldset/p[3]/button') 
    driver.execute_script("arguments[0].click();", element)                      
    time.sleep(5)

    check = Alert(driver)                            #팝업 확인
    check.accept()


def crawling():
    driver.get(board_url)
    html = driver.page_source
    soup = bs(html, 'html.parser')

    board_main = soup.find("div",  {"class" : "list"}) 
    board_body = board_main.find("tbody",  {"class" : "txtcenter"})
    board_list = board_body.find_all("tr")
    
    datas =[]

    for item in board_list:    
        board_number_all = item.find("td")                                    #자료번호    
        board_number = board_number_all.text.strip()
          
        data = item.find("td", {"class":"txtleft"})                                         
        link = data.find("a")                                                    
        link_url = link.get("href")                                        # 상세 URL
        print("https://www.nyj.go.kr/museum/4572"+ link_url)
        
        datas.append(detail("https://www.nyj.go.kr/museum/4572"+ link_url, board_number))
 
 
    if len(datas) > 0:
        db = DatabaseManager(DATABASE_ID)
        db.connection()
        print(datas)
        query = '''
                INSERT INTO board_nyj (SEQ, TITLE, READ_COUNT, LINK_URL, ATTACH_URL, WRITER, CONTENT, REG_DATE)
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            '''        

        db.execute_query_bulk(query, datas)        
                
 
        
#상세 크롤링
def detail(detail_url, board_number):
    driver.get(detail_url)  
    
    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    view_main = detail_soup.find("div",  {"class" : "proc_read"})
    view_boby = view_main.find("tbody")
    view_list = view_boby.find_all("tr")
        
    title_main = view_list[0]    
    title = title_main.find("span").text                                                 # 제목
    
    writer_main = view_list[1]
    writer = writer_main.find("td").text.strip()                                         # 작성자
          
    file = view_boby.find("ol",  {"class" : "file_list"})

    read_count_no = 4
    reg_date_no = 5
    
    if file != None:                                                                             
        read_count_no = 5
        reg_date_no = 6

    read_count = view_list[read_count_no].find("td").text                                 # 조회수
    reg_date = view_list[reg_date_no].find("td").text                                 # 등록일

    content_all = view_list[3]
    content_main = content_all.find("div",  {"class" : "board_content content_editor"})  # 내용
    content = content_main.find("p").text    
    
    attach_url= ""    
    
    
    return [board_number, title ,read_count, detail_url , attach_url, writer, content, reg_date] 

         
def main():
    
    login()
         
    crawling()
            
    driver.quit()
         
if __name__ == '__main__':
    main()