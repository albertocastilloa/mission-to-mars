# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
import re

hemisphere_image_urls = [
    {"title":"Cerberus Hemisphere Enhanced", "img_url":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    {"title":"Valles Marineris Hemisphere Enhanced", "img_url":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
    {"title":"Schiaparelli Hemisphere Enhanced", "img_url":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    {"title":"Syrtis Major Hemisphere Enhanced", "img_url":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"}
]

mars_dict = {
    "news_title":"",
    "news_teaser":"",
    "featured_image_url":"",
    "mars_weather":"",
    "mars_facts":"",
    "mars_hemis": hemisphere_image_urls
}


# # Mars Nasa
def mars_nasa():
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=1&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    #print(soup.prettify())
    news_title = soup.find('div', class_='content_title').text.strip()
    news_teaser = soup.find('div', class_='rollover_description_inner').text.strip()
    
    return news_title, news_teaser

 # Feature Mars Image
def feature_image():
    #Activate driver
    browser = Browser('chrome')

    nasa_url = 'https://www.jpl.nasa.gov'
    #images_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16217_hires.jpg'
    destiny = str(nasa_url) + "/spaceimages/?search=&category=Mars"
    #Load source
    browser.visit(destiny)
    html_source = browser.html
    #Click <Full image> pic
    browser.find_by_id('full_image').click()
    #Go to More Info
    soup = bs(html_source, 'html.parser')
    #print(soup.prettify())
    buttons = soup.find('article', class_='carousel_item')
    url_pic = '/spaceimages/images/largesize/'
    id_pic = buttons.a['data-link'] + ":"
    #Get image ID cleaning id_pic string
    m = re.search('=(.+?):', id_pic)
    if m:
        featured_image_url = nasa_url + url_pic + m.group(1) + '_hires.jpg'
        browser.visit(featured_image_url)
        
    return featured_image_url

# Mars weather tweet
def mars_tweet():
    #URL to be scraped
    url = "https://twitter.com/MarsWxReport"
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    #print(soup.prettify())
    tweet = soup.find_all('div', class_='js-tweet-text-container')
    #Get last Mars weather report
    for t in tweet:
        mars_weather = t.p.text
     
    return mars_weather
    
# # Mars facts
def mars_facts_table():
    #URL to be scraped
    url = "https://space-facts.com/mars/"
    #Retrieve table
    table = pd.read_html(url)
    #Assign table list to df
    mars_df = table[0]
    #Rename df columns
    mars_df.columns = ['description', 'value', 'delete']
    #Keep important columns
    mars_df = mars_df[['description', 'value']]
    #Set index up
    mars_df.set_index('description', inplace=True)
    #Convert df to html code and replace \n
    mars_facts = mars_df.to_html().replace("\n",'')

    return mars_facts




#Calling defs
def scrape():
    mars_dict["news_title"], mars_dict["news_teaser"] = mars_nasa()
    mars_dict["featured_image_url"] = feature_image()
    mars_dict["mars_weather"] = mars_tweet()
    mars_dict["mars_facts"] = mars_facts_table()
    return mars_dict