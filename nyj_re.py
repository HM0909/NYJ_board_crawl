from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import time
from db_manager import DatabaseManager

# 남양주시립박물관(nyj)

base_url = "https://www.nyj.go.kr/museum/4606"
board_url = "https://www.nyj.go.kr/museum/4572" 
login_url = "https://www.nyj.go.kr/main/63?referer=https%3A%2F%2Fwww.nyj.go.kr%2Fmuseum%2F4606" 

DATABASE_ID = "local"

driver = webdriver.Chrome(executable_path='C:\hm_py\chromedriver')    # Windows

def login():
    driver.get(base_url)

    # 로그인 페이지 이동
    element = driver.find_element_by_xpath('//*[@id="process_login"]')  
    driver.execute_script("arguments[0].click();", element)

    # 로그인
    user_id = ""
    user_password = ""
    
    driver.find_element_by_id('user_id').send_keys(user_id)
    time.sleep(5)
    driver.find_element_by_id('user_password').send_keys(user_password)
    time.sleep(5)
    element = driver.find_element_by_xpath('//*[@id="memberForm"]/fieldset/p[3]/button') 
    driver.execute_script("arguments[0].click();", element)                      
    time.sleep(5)
    
    # 로그인 성공 팝업_확인    
    check = Alert(driver)                         
    check.accept() 

    
def crawling():        
    driver.get(board_url)
    
    html = driver.page_source
    soup = bs(html, 'html.parser')
    
    board_main = soup.find("tbody",  {"class" : "txtcenter"}) 
    board_body = board_main.find_all("tr")

    datas =[]
    
    for list in board_body:
        board_list = list.find_all("td")
        board_number = board_list[0].text.strip()               # 글번호_공백제거

        data = list.find("td",  {"class" : "txtleft"}) 
        link = data.find("a")
        url = link.get("href")                        
        link_url = "https://www.nyj.go.kr/museum/4572" + url     # 상세 URL

        detail(board_number, link_url)

        datas.append(detail(board_number, link_url))


    if len(datas) > 0:  
                    db = DatabaseManager(DATABASE_ID)  
                    db.connection()  
                    query = '''  
                            INSERT INTO board_nyj (BD_NUMBER, LINK_URL, TITLE, WRITER, CONTENT, READ_COUNT, REG_DATE, ATTACH_URL)    
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
        
        
def detail(board_number, link_url):       
    driver.get(link_url)  
         
    detail_html = driver.page_source
    detail_soup = bs(detail_html, 'html.parser')  
 
    detail_main = detail_soup.find("tbody")
    detail_body = detail_main.find_all("tr")
    
    title_list = detail_body[0]
    title = title_list.find("span").text                         # 제목

    wirter_list = detail_body[1]
    wirter = wirter_list.find("td").text.strip()                 # 작성자
    
    content_main = detail_body[3]
    content_body = content_main.find("div",  {"class" : "board_content content_editor"}) 
    content = content_body.find("p").text                        # 내용

    attach_main = detail_body[4]
    
    attach_url = ""
    
    if attach_main.find("ol",  {"class" : "file_list"}) != None:
        attach_body = attach_main.find("ol",  {"class" : "file_list"})
        attach_list = attach_body.find_all("li")
    
        for list in attach_list:
            attach = list.find("a")
            attach_url= attach.get("href")                        # 첨부파일 URL

        read_count_no = 5
        reg_date_no = 6
        
        read_count = detail_body[read_count_no].find("td").text                                 # 조회수
        reg_date = detail_body[reg_date_no].find("td").text                                     # 등록일
        
    else:
        read_count_no = 4
        reg_date_no = 5
        
        read_count = detail_body[read_count_no].find("td").text                                 # 조회수
        reg_date = detail_body[reg_date_no].find("td").text                                     # 등록일


    return [board_number, link_url, title, wirter, content, read_count, reg_date, attach_url, ]



def main():
    
    # login()

    crawling()
    
if __name__ == '__main__':
    main()