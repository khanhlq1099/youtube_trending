import pandas as pd
from datetime import datetime,timedelta

import io
from trending.config.config import MinIO_S3_client

from trending.extract.crawler import extract_trending_data

from selenium import webdriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def extract_trending_youtube():
    def upload_df_to_s3(df:pd.DataFrame):
        current_date = datetime.today().strftime("%Y_%m_%d")
        current_time = (datetime.now() + timedelta(hours=7)).strftime("%Hh_%Mm")

        with io.StringIO() as csv_buffer:
            df.to_csv(csv_buffer,index=False)
            response = MinIO_S3_client.s3.put_object(Bucket='youtube',Key = "bronze/trending/" + current_date + "/" + current_time +".csv",Body=csv_buffer.getvalue())

            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

            if status == 200:
                print(f"Successful S3 put_object response. Status - {status}")
            else:
                print(f"Unsuccessful S3 put_object response. Status - {status}")

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

    try:
        df = extract_trending_data(driver=driver)
        # print(df)
        if df.shape[0] >= 1:
            upload_df_to_s3(df)

    except Exception as e:
        print(e)

# extract_trending_youtube()