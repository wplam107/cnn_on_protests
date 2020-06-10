import pickle
import pandas as pd
from selenium import webdriver
from webscrape_funcs import get_urls, scrape_site

if __name__ == '__main__':
    driver = webdriver.Chrome()
    args = {'query': 'protests', 'category': 'us', 'limit': 20}
    urls = get_urls(driver, args)
    driver.quit()

    driver = webdriver.Chrome()
    scraped_urls, dates, headlines, bodies = scrape_site(urls, driver)
    df = pd.DataFrame()
    df['headline'] = headlines
    df['body'] = bodies
    df['date'] = dates
    df['url'] = scraped_urls
    driver.quit()

    f = open('floyd_protests.p', 'wb')
    pickle.dump(df, f)
    f.close()