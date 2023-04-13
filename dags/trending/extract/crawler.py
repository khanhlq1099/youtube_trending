import pandas as pd
import requests
from time import sleep
from datetime import datetime,timedelta

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from bs4 import BeautifulSoup

import trending.lib.video_helper as vh

# Get option in trending tab
def extract_trending_data(driver: webdriver.Chrome = None) -> pd.DataFrame:
    if driver is None:
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.binary_location = "/Users/lamquockhanh10/VSCodeProjects/kpim_stock/stock_etl/stock/lib/chromedriver"
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument('--disable-dev-shm-usage') 
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument('--disable-gpu')
        # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        driver = webdriver.Remote("http://selenium:4444/wd/hub",desired_capabilities=DesiredCapabilities.CHROME,options=chrome_options)

    driver.implicitly_wait(10)
    driver.set_page_load_timeout(60)

    driver.get('https://www.youtube.com/feed/trending')

    # tab = driver.find_element(By.XPATH,'//*[@class="tab-title style-scope ytd-c4-tabbed-header-renderer"]')
    tabs = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="tab-title style-scope ytd-c4-tabbed-header-renderer"]')))
    tabs = driver.find_elements(By.XPATH,'//*[@class="tab-title style-scope ytd-c4-tabbed-header-renderer"]')

    all_rows = []

    for tab in tabs:
        tab.click()
        sleep(2)
        all_row = extract_data_by_option(tab,driver)
        all_rows.extend(all_row)

    driver.quit()
    df = pd.DataFrame(all_rows)
    # df.to_csv('/Users/lamquockhanh10/VSCodeProjects/youtube_trending/trending.csv',index=False)
    print(df)
    return df
    
    
# Get data for each option
def extract_data_by_option(tab:WebElement,driver:WebElement):

    list_video = driver.find_element(By.XPATH,'//*[@class="style-scope ytd-expanded-shelf-contents-renderer"]')

    soup = BeautifulSoup(list_video.get_attribute('innerHTML'),"html.parser")
    # print(soup)
    videos = soup.find_all('ytd-video-renderer', attrs={"class":"style-scope ytd-expanded-shelf-contents-renderer"})
    # print(videos)
    rows = []
    x = 1
    def extract_video_info(x,video):
        vid_dict = {}
        vid_dict["top_trending"] = x
        vid_dict["video_title"] = video.find('yt-formatted-string',attrs={"class":"style-scope ytd-video-renderer"}).text

        video_link = video.find('a',attrs={"id":"thumbnail"})['href']
        vid_dict["video_id"] = vh.video_helper(video_link)
        vid_dict["video_link"] = 'youtube.com' + video_link
        
        vid_dict["chanel_name"] = video.find('a',attrs={"class":"yt-simple-endpoint style-scope yt-formatted-string"}).text
        vid_dict["chanel_link"] = 'youtube.com' + video.find('a',attrs={"class":"yt-simple-endpoint style-scope yt-formatted-string"})['href']

        string_views = video.find_all('span',attrs={"class":"inline-metadata-item style-scope ytd-video-meta-block"})[0].text
        vid_dict["views"] = vh.views_helper(string_views)

        upload_date = video.find_all('span',attrs={"class":"inline-metadata-item style-scope ytd-video-meta-block"})[1].text
        vid_dict["uploaded_date"] = vh.date_helper(upload_date)

        type = video.find('span',attrs = {"class":"style-scope ytd-thumbnail-overlay-time-status-renderer"}).text.strip()
        vid_dict["video_type"] = vh.type_helper(type)

        vid_dict["tab"] = tab.text
        vid_dict["etl_date"] = datetime.today().strftime('%Y-%m-%d')
        vid_dict["etl_time"] = (datetime.now() + timedelta(hours=7)).strftime("%H:%M:%S")

        return vid_dict
    for video in videos:
        row = extract_video_info(x,video) 
        x+=1
        rows.append(row) 
    return rows
