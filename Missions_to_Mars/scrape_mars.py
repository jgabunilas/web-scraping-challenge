from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time
import datetime as dt

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

        # The featured image URL lies within an article tag under a style attribute. However, this soup find will return a partial URL that has unneeded information. This extraneous information will need to be sliced out of the string. Regardless of how long the URL is, we can get at the part that we care about by slicing from the 23rd character to the third-to-last character.
        # Note that the featured image is sometimes unrelated to Mars, in spite of being featured on the Mars space images page.
        featured_image = soup.find('article')['style']
        # featured_image[23:-3]

        # The featured image URL can be completed by adding the featured_image slice to the base URL.
        featured_image_url = f'https://www.jpl.nasa.gov' + featured_image[23:-3]
        # featured_image_url


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
        mars_facts_html = mars_facts_df.to_html(index=False, border=2, justify='left')
        # mars_facts_df
        # Save the mars_facts HTML code to the dictionary
        mars_data['mars_facts_html'] = mars_facts_html

        ## Mars Hemispheres
        # Initiate an empty list for the title and img_url dictionaries
        hemisphere_image_urls = []
        
        # Create a list of each of the enhanced hemisphere pages that will need to be scraped
        urls = [
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
        ]

        # Scrape the image URLs using a for loop to iterate though each respective page and dig up the image URL for the hemisphere and the title of the hemisphere
        for url in urls:
                executable_path = {'executable_path': 'chromedriver.exe'}
                browser = Browser('chrome', **executable_path, headless=False)
                browser.visit(url)

                time.sleep(5)
                html = browser.html
                soup = bs(html, "html.parser")


                title = soup.find('h2', class_='title').text
                img_url = 'https://astrogeology.usgs.gov'+soup.find('img', class_='wide-image')['src']
                # print(title)
                # print(img_url)

                # Append the scraped title and image url to the hemisphere_image_urls dictionary
                hemisphere_image_urls.append(
                        {
                        'title': title,
                        'img_url': img_url
                        }
                )
        

        # Add hemisphere image dictionary to the mars_data dictionary
        mars_data['hemisphere_image_urls'] = hemisphere_image_urls
        
        # Add the time of the scrape to the dictionary
        mars_data['last_scrape'] = dt.datetime.now()

        return mars_data

# print(scrape())