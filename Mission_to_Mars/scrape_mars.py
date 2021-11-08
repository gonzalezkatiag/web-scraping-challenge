from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

# Scrape
def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    results  = {}
    
    ## MARS NEWS ##
    # URL
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)

    # HTML parser
    html = browser.html
    news_mars = BeautifulSoup(html, 'html.parser')

    news_title = news_mars.body.find('div', class_='content_title').text
    news_desc = news_mars.body.find('div', class_='article_teaser_body').text

    ## MARS IMAGE ##
    # URL
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    # HTML parser
    html = browser.html
    mars_image = BeautifulSoup(html, 'html.parser')

    # Scrape image url
    image_relative_path = mars_image.find_all('img', class_='headerimage fade-in')[0]["src"]
    featured_image_url = f"{image_url}{image_relative_path}"

    # MARS FACTS ##
    fact_url = 'https://galaxyfacts-mars.com/'
    browser.visit(fact_url)

    # HTML parser
    html = browser.html
    mars_facts = BeautifulSoup(html, 'html.parser')

    # Convert info into DataFrame
    mars_table = pd.read_html(fact_url)

    # Convert to table
    mars_table_df = pd.DataFrame(mars_table[0])
    mars_table_df.columns = ["Element", "Mars", "Earth"]

    # Convert to html string
    mars_html = mars_table_df.to_html()

    ## HEMISPHERES ##
    # URL
    mars_hems_url = 'https://marshemispheres.com/'
    browser.visit(mars_hems_url)

    # Create dictionary
    img_link_dict = {}

    # HTML parser
    html = browser.html
    mars_hems_image = BeautifulSoup(html, 'html.parser')
    results = mars_hems_image.find_all('div', class_='description')
    
    links = browser.links.find_by_partial_text("Hemisphere Enhanced")

    mers_hems_list = []

    for index, link in enumerate(links):
        img_link_dict = {}
        if index > 0:
            browser.back()
            time.sleep(2)
            links = browser.links.find_by_partial_text("Hemisphere Enhanced")
    link = links[index]
    title = link.text
    link.click()
    time.sleep(1)
    inner_html = browser.html
    inner_soup = BeautifulSoup(inner_html, 'html.parser')
    downloads = inner_soup.find('div', class_='downloads')

    img_link_dict['title'] = f'{title}'
    img_link_dict['link'] = f"{mars_hems_url}{downloads.find('a')['href']}"
    mers_hems_list.append(img_link_dict)
    
    results = {
       'latest_title': news_title,
       'latest_desc': news_desc,
       'image_mars': featured_image_url,
       'facts_table': str(mars_html),
       'hemisphere_img_url': mers_hems_list
    }

    # Stop browser
    browser.quit()
    
    return results