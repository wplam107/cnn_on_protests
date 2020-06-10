import pickle
import pandas as pd
from selenium import webdriver
from webscrape_funcs import get_urls, scrape_site

# Rescrape HK protest articles from CNN
if __name__ == '__main__':
    f = open('cnn_urls.p', 'rb')
    hk_urls = pickle.load(f)
    f.close()

    driver = webdriver.Chrome()
    scraped_urls, dates, headlines, bodies = scrape_site(hk_urls, driver)
    df = pd.DataFrame()
    df['headline'] = headlines
    df['body'] = bodies
    df['date'] = dates
    df['url'] = scraped_urls
    driver.quit()

    f = open('hk_protests.p', 'wb')
    pickle.dump(df, f)
    f.close()