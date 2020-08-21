from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time


def scrape():
        # Initialize the mars_data dictionary
        mars_data = {}
        url = 'https://mars.nasa.gov/news/'


        # Chromedriver executable path
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)

        time.sleep(5)
        html = browser.html
        soup = bs(html, "html.parser")
        # print(soup.prettify())

        ## Latest News

        # Get the latest news item, which is the first instance of the div of class "list_text". Then search within the news_item
        latest_news_item = soup.find('div', class_="list_text")
        news_title = latest_news_item.find('div', class_="content_title").text
        news_paragraph = latest_news_item.find('div', class_="article_teaser_body").text
        # print(news_title)
        # print(news_paragraph)

        # Add the news title and news paragraph to the mars_data dictionary
        mars_data['news_title'] = news_title
        mars_data['news_paragraph'] = news_paragraph

        ## Latest Image

        # Load in the JPL Mars images website and open with splinter
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)

        # Soupify the browser
        time.sleep(5)
        html = browser.html
        soup = bs(html, "html.parser")

        # The latest Mars image on this page will be referenced in the first instance of the list item of class "slide"
        latest_mars_image = soup.find('li', class_='slide')
        # print(latest_mars_image.prettify())
        # print('-------------')
        # The high-res image URL is contained within the property 'data-fancybox-href', which itself is within the first anchor tag of the list element.
        image_tag = latest_mars_image.find('a')['data-fancybox-href']

        # Complete the image URL by adding the base URL to the image_tag
        featured_image_url = f'https://www.jpl.nasa.gov' + image_tag
        # print(featured_image_url)
        # Save the image URL into the mars_data dictionary
        mars_data['featured_image_url'] = featured_image_url

        ## Mars Facts
        # Set url for Mars Facts website
        url = 'https://space-facts.com/mars/'
        mars_facts = pd.read_html(url)
        # Convert to a dataframe
        mars_facts_df = mars_facts[0]
        # Update Column Names
        mars_facts_df = mars_facts_df.rename(columns = {0:'Property', 1:'Value'})
        mars_facts_html = mars_facts_df.to_html(index=False)
        # mars_facts_df
        # Save the mars_facts HTML code to the dictionary
        mars_data['mars_facts_html'] = mars_facts_html

        ## Mars Hemispheres
        # Create a list of dictionaries containing of the Mars hemisphere titles and full resolution image URLs
        hemisphere_image_urls = [
        {
                'title':'Valles Marineris Hemisphere',
                'img_url':'https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg'
        },
        {
                'title':'Cerberus Hemisphere',
                'img_url':'https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg'
        },
        {
                'title':'Schiaparelli Hemisphere',
                'img_url':'https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg'        
        },
        {
                'title':'Syrtis Major Hemisphere',
                'img_url':'https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg' 
        }
        ]        

        # Add hemisphere image dictionary to the mars_data dictionary
        mars_data['hemisphere_image_urls'] = hemisphere_image_urls

        return mars_data

# print(scrape())