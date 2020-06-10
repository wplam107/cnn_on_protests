import time
import re

def scrape_page_urls(driver):
    """
    Scrape all URLs on a CNN search page.  Requires instantiated webdriver.
    """

    page_urls = []
    xpath = '/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[3]/div[{}]/div[2]/h3/a'

    for i in range(1, 11):
        href = driver.find_element_by_xpath(xpath.format(i)).get_attribute('href')
        if re.search('live-news', href):
            continue
        else:
            page_urls.append(href)

    return page_urls

def get_urls(driver, args={'query': None, 'category': None, 'limit': None}):
    """
    Load search pages from CNN.

    Parameters
    ----------
    driver : webdriver instance
    args : dictionary of search arguments
    """

    urls = []

    # Get first page of urls
    if args['category']:
        driver.get(f"https://www.cnn.com/search?q={args['query']}&size=10&category={args['category']}&type=article")
    else:
        driver.get(f"https://www.cnn.com/search?q={args['query']}&size=10&type=article")

    time.sleep(1)
    page_urls = scrape_page_urls(driver)
    urls += page_urls

    # Get remaining page urls
    for i in range(2, args['limit'] + 1):
        driver.get(f'https://www.cnn.com/search?q=protests&size=10&page={i}&from={(i-1)*10}&category=us&type=article')
        time.sleep(1)
        page_urls = scrape_page_urls(driver)
        urls += page_urls
    
    return urls

def scrape_article(url, driver):
    """
    Function to scrape article headline, date, and body
    """

    driver.get(url)
    body = []
    time.sleep(3)

    # Click modal button
    try:
        modal_button = driver.find_element_by_class_name('bx-close bx-close-link bx-close-inside')
        modal_button.click()
    except:
        pass
    
    # Get date
    try:
        date = driver.find_element_by_class_name('update-time').text
    except:
        date = ''
    
    # Get headline
    try:
        headline = driver.find_element_by_class_name('pg-headline').text
    except:
        headline = ''

    # Get body excluding byline
    try:
        texts = driver.find_elements_by_class_name('zn-body__paragraph')
        for text in texts:
            if re.search('CNN\'s', text.text):
                continue
            else:
                body.append(text.text)
    except:
        body.append('')
    
    body = ' '.join(body)
        
    return url, date, headline, body

def scrape_site(urls, driver, ret_csv=False, csv=''):
    new_urls = []
    dates = []
    headlines = []
    bodies = []
    
    for url in urls:
        time.sleep(1)
        url, date, headline, body = scrape_article(url, driver)
        new_urls.append(url)
        dates.append(date)
        headlines.append(headline)
        bodies.append(body)
    
    if ret_csv == True:
        df.to_csv(csv, sep='\t')
        print(f'File {csv} Created')
    return new_urls, dates, headlines, bodies