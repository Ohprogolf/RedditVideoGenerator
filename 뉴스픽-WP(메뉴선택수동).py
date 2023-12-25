# -*- coding: utf-8 -*-

from time import sleep
import datetime
import time
import requests
#import schedule
from time import gmtime
from time import strftime
from selenium.webdriver.common.by import By
import subprocess
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import platform
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from fake_useragent import UserAgent
from pprint import pprint as pp
import ssl
import json
from urllib import request
from urllib import parse
import openpyxl
from datetime import datetime

C_END = "\033[0m"
C_BOLD = "\033[1m"
C_INVERSE = "\033[7m"
C_BLACK = "\033[30m"
C_RED = "\033[31m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_PURPLE = "\033[35m"
C_CYAN = "\033[36m"
C_WHITE = "\033[37m"
C_BGBLACK = "\033[40m"
C_BGRED = "\033[41m"
C_BGGREEN = "\033[42m"
C_BGYELLOW = "\033[43m"
C_BGBLUE = "\033[44m"
C_BGPURPLE = "\033[45m"
C_BGCYAN = "\033[46m"
C_BGWHITE = "\033[47m"

# [사용자 입력 정보]
# ======================================================================================================== START

# 카카오 ID/PW
kakao_id = ""
kakao_pw = ""

# 본인추천인 코드
referral_code = "d3yMo16A&cp=H0cKa48w"
#referral_code = "d3yMo16A"

# 가져오려는 컨텐츠의 수 (개발자 도구에서 netowrk 를 통해 분석된 contentList 에는 추천(recomList)과 일반(contentList) 컨텐츠들이 있음)
# 그런데 여기서 기본적으로 추천 컨텐츠는 10개를 가져오게 되고 나머지 일반 컨텐츠들은 아래의 수에 의해 가져오는 수가 결정됨
GET_CONTENTS_NUM = 3  # 결국 여기 있는 수에 10을 더한수가 전체 컨텐츠 수입니다.

# 카테고리 랜덤 여부
CATEGORY_RAMDOM = False

# 만약 카테고리 선택을 랜덤으로 하지 않는 경우 카테고리 중 하나 선택('메인'과 '쇼핑'은 대상에서 제외)
# newspick_category_kr = ['유머', '스토리', '응큼세포', '아이돌', '연예가화제', '정치', '경제', '사회', '사건사고', 'TV연예', '영화', 'K-뮤직',
#                         '스포츠', '축구', '야구', '반려동물', '생활픽', '해외연예', 'BBC News', 'NNA코리아', '글로벌']
# newspick_category = ['24', '50', '35', '28', '36', '31', '14', '32', '12', '51', '53', '57', '7', '15', '16',
#                      '3', '33', '58', '11', '38', '39']
newspick_category_kr = '유머'
newspick_category = '24'

# pause time 정보
# PAUSE_TIME = 0.5
# LOADING_WAIT_TIME = 5
# GET_NEWSPICK_LINK_TIME = 2
PAUSE_TIME = 0.1
LOADING_WAIT_TIME = 2
GET_NEWSPICK_LINK_TIME = 1
#WRITE_WAITTIME = 900  # 밴드포스팅 간격

# # fake-useragent / user-agent
# # https://domdom.tistory.com/329
# # ua = UserAgent(use_cache_server=True)
# ua = UserAgent(verify_ssl=False)
# user_agent = ua.random
# print(f'User-Agent : {user_agent}')
fixed_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Whale/3.19.166.16 Safari/537.36'

# [사용자 입력 정보]
# ======================================================================================================== END

# [시스템 공통 입력 정보]
# ======================================================================================================== START

# 뉴스픽 정보  https://partners.newspic.kr/main/contentList, 카테고리별(ex. channelNo=12, 사건사고) 로 가져오는 정보
recommand_nid_lists = []
recommand_providerNo_lists = []
recommand_recomType_lists = []
recommand_title_lists = []

content_nid_lists = []
content_providerNo_lists = []
content_recomType_lists = []
content_title_lists = []

# 최종 shorten 링크가 저장될 리스트
recommand_shorten_lists = []
recommand_imgUrl_lists = []
content_shorten_lists = []
content_imgUrl_lists = []

# 추천 정보와 일반 정보를 합친 리스트
reco_cont_title_lists = []
reco_cont_shorten_lists = []
reco_cont_imgUrl_lists = []

# 실시간 검색 순위 해시 태그 리스트
hash_tag_lists = []

global xl_data

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pyperclip
import pyautogui
import openpyxl
from datetime import datetime

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

LOADING_WAIT_TIME = 1  # 필요에 따라 적절한 로딩 대기 시간 설정

def init_driver():
    chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
    options = Options()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(service=chrome_service, options=options)
    print("드라이버 초기화 완료")  # 로그 추가

    return driver

###################################################################################################################

def newspic_login(driver):
    driver.get('https://partners.newspic.kr/login')
    driver.implicitly_wait(2)
    # driver.maximize_window()
    time.sleep(2)

    id = driver.find_element(By.NAME, 'id')
    id.click()
    pyperclip.copy('jj.wiki1004@gmail.com')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    pw = driver.find_element(By.NAME, 'password')
    pw.click()
    pyperclip.copy('670904!ohN')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    login_btn = driver.find_element(By.XPATH, '/html/body/div[1]/section/div[2]/div/div[1]/form/button')
    login_btn.click()
    time.sleep(2)

    return driver  # 이 부분 추가 

###################################################################################################################

def get_cookies_session(driver, url):
    driver.get(url)
    sleep(LOADING_WAIT_TIME)

    _cookies = driver.get_cookies()
    cookie_dict = {}
    for cookie in _cookies:
        cookie_dict[cookie['name']] = cookie['value']
    #print(cookie_dict)

    _session = requests.Session()
    headers = {
        'User-Agent': fixed_user_agent,
    }
    #print(_session.headers)
    #print(_session.cookies)

    _session.headers.update(headers)  # User-Agent 변경
    #print(_session.headers)

    _session.cookies.update(cookie_dict)  # 응답받은 cookies로  변경
    #print(_session.cookies)

    return _session

###################################################################################################################################
def get_newspick_info(_session, category_num, category_kr):
    url = f'https://partners.newspic.kr/main/contentList?channelNo={category_num}&inputSwitch=false&adultContentCheck=N&totalRow=0&pageSize={GET_CONTENTS_NUM}'
    with _session as s:
        data = s.post(url).json()
        # pp(data)

    try:
        print(f'\n카테고리 "{category_kr}"의 [추천] 컨텐츠들은 총 {len(data["recomList"])}개 있습니다. 그 내용은 아래와 같습니다.')
        #for num in range(len(data['recomList'])):
        for num in range(1,1):  
            nid = data['recomList'][num]['nid']  # nid
            providerNo = data['recomList'][num]['providerNo']  # pn
            recomType = data['recomList'][num]['recomType']  # rssOtion
            title = data["recomList"][num]["title"]
            
            imgUrl = data["recomList"][num]["imgUrl"] ################## 추가

            recommand_nid_lists.append(nid)
            recommand_providerNo_lists.append(providerNo)
            recommand_recomType_lists.append(recomType)
            recommand_title_lists.append(title)
            recommand_imgUrl_lists.append(imgUrl)
            print(
                #f'{num + 1}. {data["recomList"][num]["title"]} | {data["recomList"][num]["link"]} | {nid} | {providerNo} | {recomType}')
            f'{num + 1}. {data["recomList"][num]["title"]} | {data["recomList"][num]["link"]} | {nid} | {providerNo} | {recomType} | {data["recomList"][num]["imgUrl"]}')

    except:
        print("[추천] 컨텐츠들이 없거나 예상치 못한 에러입니다.]")
        print(f"에러 발생: {e}")

    try:
        print(f'\n카테고리 "{category_kr}"의 [일반] 컨텐츠들은 총 {len(data["contentList"])}개 있습니다. 그 내용은 아래와 같습니다.')
        for num in range(len(data['contentList'])):
            nid = data['contentList'][num]['nid']  # nid
            providerNo = data['contentList'][num]['providerNo']  # pn
            recomType = data['contentList'][num]['recomType']  # rssOtion
            title = data['contentList'][num]['title']

            imgUrl = data["contentList"][num]["imgUrl"]  ################## 추가

            content_nid_lists.append(nid)
            content_providerNo_lists.append(providerNo)
            content_recomType_lists.append(recomType)
            content_title_lists.append(title)
            content_imgUrl_lists.append(imgUrl)
            print(
                #f'{num + 1}. {data["contentList"][num]["title"]} | {data["contentList"][num]["link"]} | {nid} | {providerNo} | {recomType}')
                f'{num + 1}. {data["contentList"][num]["title"]} | {data["contentList"][num]["link"]} | {nid} | {providerNo} | {recomType} | {data["contentList"][num]["imgUrl"]}')

    except:
        print("[일반] 컨텐츠들이 없거나 예상치 못한 에러입니다.]")
        print(f"에러 발생: {e}")

#########################################################################################################################

def get_newspick_link(_session, category_num, category_kr):
    count = 1

    # for recomList
    print(
        f'\n카테고리 "{category_kr}"의 [추천] 컨텐츠들은 총 {len(recommand_recomType_lists)}개 있습니다. [뉴스픽 개인 링크 생성 중입니다.]. request 한도 때문에 천천히 request 시도... 1분 30초')
    #for i in range(len(recommand_recomType_lists)):
    for num in range(1,1):      
        # '?nid=2023022322222268617&pn=641&cp=N9CTh50j&utm_medium=affiliate&utm_campaign=2023022322222268617&rssOption=CTR&channelName=%EC%9C%A0%EB%A8%B8&channelNo=24&sharedFrom=CT-R-L&utm_source=np220822N9CTh50j'
        url = f'https://partners.newspic.kr/management/share/getShortUrl?queryString=%3F' \
              f'nid%3D{recommand_nid_lists[i]}%26' \
              f'pn%3D{recommand_providerNo_lists[i]}%26' \
              f'cp%3D{referral_code}%26' \
              f'utm_medium%3Daffiliate%26' \
              f'utm_campaign%3D{recommand_nid_lists[i]}%26' \
              f'rssOption%3D{recommand_recomType_lists[i]}%26' \
              f'channelName%3D{category_kr}%26' \
              f'channelNo%3D{category_num}%26' \
              f'sharedFrom%3DCT-R-L%26' \
              f'utm_source%3Dnp220822{referral_code}'
        with _session as s:
            data = s.get(url)
            shorten_url = f'https://bltly.link/{data.text}'
            print(f'{i + 1}. https://bltly.link/{data.text}')
            recommand_shorten_lists.append(shorten_url)
            sleep(GET_NEWSPICK_LINK_TIME)  # 1분 대기
            count = count + 1

    # for contentList
    print(
        f'\n카테고리 "{category_kr}"의 [일반] 컨텐츠들은 총 {len(content_recomType_lists)}개 있습니다. [뉴스픽 개인 링크 생성 중입니다.]. request 한도 떄문에 천천히 request 시도... 1분 30초')
    for j in range(len(content_recomType_lists)):
        # '?nid=2023022400274854744&pn=641&cp=N9CTh50j&utm_medium=affiliate&utm_campaign=2023022400274854744&channelName=%EC%9C%A0%EB%A8%B8&channelNo=24&sharedFrom=CT-NO-L&utm_source=np220822N9CTh50j'
        url = f'https://partners.newspic.kr/management/share/getShortUrl?queryString=%3F' \
              f'nid%3D{content_nid_lists[j]}%26' \
              f'pn%3D{content_providerNo_lists[j]}%26' \
              f'cp%3D{referral_code}%26' \
              f'utm_medium%3Daffiliate%26' \
              f'utm_campaign%3D{content_nid_lists[j]}%26' \
              f'channelName%3D{category_kr}%26' \
              f'channelNo%3D{category_num}%26' \
              f'sharedFrom%3DCT-NO-L%26' \
              f'utm_source%3Dnp220822{referral_code}'
        with _session as s:
            data = s.get(url)
            shorten_url = f'https://bltly.link/{data.text}'
            print(f'{j + 1}. https://bltly.link/{data.text}')
            content_shorten_lists.append(shorten_url)
            sleep(GET_NEWSPICK_LINK_TIME)  # 1분 대기
            count = count + 1

    # title 과 url 리스트 합치기
    global reco_cont_title_lists
    global reco_cont_shorten_lists
    global reco_cont_imgUrl_lists

    reco_cont_title_lists = recommand_title_lists + content_title_lists
    reco_cont_shorten_lists = recommand_shorten_lists + content_shorten_lists
    reco_cont_imgUrl_lists = recommand_imgUrl_lists + content_imgUrl_lists

    print(reco_cont_title_lists)
    print(reco_cont_shorten_lists)
    print(reco_cont_imgUrl_lists)


# HTML 작성
##############################################################
def data_info(category_kr, reco_cont_title_lists, reco_cont_shorten_lists, reco_cont_imgUrl_lists):

    # now = datetime.now()
    # xl_filename = '뉴스픽_' + now.strftime('%Y%m%d%H%M%S') + '.xlsx'
    # wb = openpyxl.Workbook()
    # ws = wb.active
    # ws.append(['No', '기사 URL'])
    
    # row = 2
    # num = 1
    
    l_cat = []
    l_title = []
    l_Slink = []
    l_imglink = []
    post_content = []
    category = []
    Maxrows = len(reco_cont_shorten_lists)
    
    for num in range(len(reco_cont_shorten_lists)):
        cat = f'{category_kr}'
        title = f'{reco_cont_title_lists[num]}'
        Slink = f'{reco_cont_shorten_lists[num]}'
        imglink = f'{reco_cont_imgUrl_lists[num] if num < len(reco_cont_imgUrl_lists) else ""}'
        
        ############ 리스트생성 ###########################
        l_cat.append(cat) 
        l_title.append(title)
        l_Slink.append(Slink)
        l_imglink.append(imglink)
        ##################################################
        print(f'\n{num + 1}. {reco_cont_title_lists[num]}')

    row_html = 1
    data = []
    aTitle = []

    # E2부터 셀값을 HTML 코드로 조합하여 추가
    for row_html in range(len(reco_cont_shorten_lists)):
        html_code = '<!-- wp:image {"width":"640px","height":"360px","scale":"cover","sizeSlug":"large","linkDestination":"custom"} --><!-- /wp:image -->' \
                    f'!<!-- wp:paragraph -->' \
                    f'<table style="border-collapse: collapse; width: 95.4663%; height: 409px;">' \
                    f'<tbody>' \
                    f'<tr style="height: 367px;">' \
                    f'<td style="width: 100%; height: 367px;"><a href="{l_Slink[row_html]}">' \
                    f'<img class="alignnone size-medium" src="{l_imglink[row_html]}" width="640" height="360" /></a></td>' \
                    f'</tr>' \
                    f'<tr style="height: 24px;">' \
                    f'<td style="width: 100%; height: 24px; text-align: left;"><a href="{l_Slink[row_html]}">' \
                    f'<strong><span style="font-family: geneva, sans-serif;">' \
                    f'<span style="font-size:14pt;">기사보기</span> →"{l_title[row_html]}"</span></strong></a></td>' \
                    f'</tr>' \
                    f'</tbody>' \
                    f'</table>' \
                    f'<!-- /wp:paragraph -->'

        data.append(html_code)
        l_title.append(title)
        category.append(cat)

   # WordPress 정보 설정
    wordpress_url = 'https://news.progoh.com/xmlrpc.php'
    wordpress_username = 'ohprogolf'
    wordpress_password = 'dolvin2k!'

    client = Client(wordpress_url, wordpress_username, wordpress_password)

    for num in range(0, Maxrows):
        post_content = data[num]
        upload_to_wordpress(client, category[num], l_title[num], post_content, num)

def upload_to_wordpress(client, category, l_title, post_content, num):
    # 카테고리 설정
    if category == '유머':
        category = '유머'
    elif category == '스토리' or category == '반려동물':
        category = '스토리'
    elif category == '사회' or category == '사건사고' or category == '생활픽':
        category = '사회'
    elif category == 'TV연예' or category == '해외연예' or category == '아이돌' or category == '연예가화제':
        category = '연예'
    elif category == '정치' or category == '경제':
        category = '정치/경제'
    elif category == '스포츠' or category == '축구' or category == '야구':
        category = '스포츠'
    elif category == '영화' or category == 'K-뮤직':
        category = '영화/음악'
    elif category == 'BBC News' or category == 'NNA코리아' or category == '글로벌':
        category = '국제'
    else:
        category = '기타'

      # 글 등록
    post = WordPressPost()
    post.title = l_title
    post.content = post_content
    post.terms_names = {'category': [category]}
    post.post_type = 'post'
    post.post_status = 'publish'
    
    try:
        client.call(NewPost(post))
        print(f"Post {num+1} has been successfully posted.")
        # 화면에 게시 성공 메시지 출력
    except Exception as e:
        print(f"Error posting the {num}-th post: {e}")
        # 화면에 게시 실패 메시지 출력

##################################################################################################################
# main start 
##################################################################################################################    
def main():
    while True:
        pass    
    
        try:
            #사용자에게 카테고리 선택 받기
            newspick_category_kr = ['유머', '스토리', '응큼세포', '아이돌', '연예가화제', '정치', '경제', '사회', '사건사고', 'TV연예', '영화', 'K-뮤직', '스포츠', '축구', '야구', '반려동물', '생활픽', '해외연예', 'BBC News', 'NNA코리아', '글로벌']
            newspick_category = ['24', '50', '35', '28', '36', '31', '14', '32', '12', '51', '53', '57', '7', '15', '16', '3', '33', '58', '11', '38', '39']

            print("다음은 가능한 카테고리 목록입니다:")
            for idx, category_kr in enumerate(newspick_category_kr):
                print(f"{idx + 1}. {category_kr}")

            selected_category_idx = int(input("카테고리 번호를 선택하세요: ")) - 1
            selected_newspick_category_kr = newspick_category_kr[selected_category_idx]
            selected_newspick_category = newspick_category[selected_category_idx]

            global g_cat 
            g_cat = selected_newspick_category_kr

            print(f'선택한 카테고리: {selected_newspick_category_kr} ({selected_newspick_category})')
    #################################################################################################################
            # start_time = time.time()  # 시작 시간 체크
            # #now = datetime.datetime.now()
            # #print("START TIME : ", now.strftime('%Y-%m-%d %H:%M:%S'))
            # print("\nSTART...")

            global recommand_nid_lists
            recommand_nid_lists = []
            global recommand_providerNo_lists
            recommand_providerNo_lists = []
            global recommand_recomType_lists
            recommand_recomType_lists = []
            global recommand_title_lists
            recommand_title_lists = []
            global content_nid_lists
            content_nid_lists = []
            global content_providerNo_lists
            content_providerNo_lists = []
            global content_recomType_lists
            content_recomType_lists = []
            global content_title_lists
            content_title_lists = []

            # 최종 shorten 링크가 저장될 리스트
            global recommand_shorten_lists
            recommand_shorten_lists = []
            global content_shorten_lists
            content_shorten_lists = []

            # 추천 정보와 일반 정보를 합친 리스트
            global reco_cont_title_lists
            reco_cont_title_lists = []
            global reco_cont_shorten_lists
            reco_cont_shorten_lists = []

            print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 시작]', C_END)
            driver = init_driver()
            sleep(PAUSE_TIME)
            print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 완료]', C_END)

            if CATEGORY_RAMDOM:
                # newspick_category_kr = ['유머', '스토리', '응큼세포', '아이돌', '연예가화제', '정치', '경제', '사회', '사건사고', 'TV연예', '영화', 'K-뮤직',
                #                         '스포츠', '축구', '야구', '반려동물', '생활픽', '해외연예', 'BBC News', 'NNA코리아', '글로벌']
                # newspick_category = ['24', '50', '35', '28', '36', '31', '14', '32', '12', '51', '53', '57', '7', '15', '16',
                #                      '3', '33', '58', '11', '38', '39']

                newspick_category_kr = ['유머', '스토리', '아이돌']
                newspick_category = ['24', '50', '28']

                # newspick_category_kr = ['응큼세포', '연예가화제', '아이돌', '연예', '꿀팁', '생활픽', '글로벌']
                # newspick_category = ['35', '36', '28', '6', '23', '33', '39']

                rand_num = random.randrange(len(newspick_category))
                rand_newspick_category = newspick_category[rand_num]
                rand_newspick_category_kr = newspick_category_kr[rand_num]
                print(
                    f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}RANDOM info >>> rand_num [{rand_num}] | rand_newspick_category [{rand_newspick_category}]| rand_newspick_category_kr [{rand_newspick_category_kr}{C_END}]')
            else:
                #rand_newspick_category_kr = '유머'
                #rand_newspick_category = '24'
                rand_newspick_category_kr = selected_newspick_category_kr
                rand_newspick_category = selected_newspick_category
                print(
                    f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}RANDOM info >>> newspick_category [{rand_newspick_category}]| newspick_category_kr [{rand_newspick_category_kr}]{C_END}')

            print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[뉴스픽 로그인 시작]', C_END)
            newspic_login(driver)
            sleep(PAUSE_TIME)
            print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[뉴스픽 로그인 완료]', C_END)

            print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[뉴스픽 로그인 후 쿠키값 저장 및 세션 리턴 시작]', C_END)
            newspick_session = get_cookies_session(driver, 'https://partners.newspic.kr/')
            sleep(PAUSE_TIME)
            print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[뉴스픽 로그인 후 쿠키값 저장 및 세션 리턴 완료]', C_END)

            print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[세션 정보를 이용하여 뉴스픽 데이터를 가져오기 시작]', C_END)
            get_newspick_info(newspick_session, rand_newspick_category, rand_newspick_category_kr)
            print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[세션 정보를 이용하여 뉴스픽 데이터를 가져오기 완료]', C_END)
            driver.quit()
            print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[뉴스픽 단축 링크 가져오기 시작]', C_END)
            get_newspick_link(newspick_session, rand_newspick_category, rand_newspick_category_kr)
            sleep(PAUSE_TIME)
            print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[뉴스픽 단축 링크 가져오기 완료]', C_END)
            
            ### 엑셀저장 & WP 포스팅 데이터 수집
            data_info(rand_newspick_category_kr,reco_cont_title_lists,reco_cont_shorten_lists,reco_cont_imgUrl_lists)
            
        finally:
            print("\n종료...")

        repeat = input("작업을 계속 반복하시겠습니까? (Y/N): ")

     # 사용자가 "N"을 입력하면 반복 종료
        if repeat.upper() == "N":
            break   
    
# main end

if __name__ == '__main__':
    main()
    # schedule.every().day.at('09:30:00').do(main)
    # schedule.every().day.at('15:30:00').do(main)
    # schedule.every().day.at('21:30:00').do(main)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
