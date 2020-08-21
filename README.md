# Web Scraping Challenge


The purpose of this challenge was to exercise mongoDB, PyMongo, Flask, Splinter, Pandas and BeautifulSoup to accomplish the following tasks:


* Use Splinter to connect to URLs on the web
* Use BeautifulSoup and Pandas to scrape target data from these web pages
* Use PyMongo to pass the scraped data into a mongo database
* Use Flask to create a dynamic website that utilizes the information from the mongo database


The subject matter for this challenge is the planet Mars. The sections below describe the specific objectives and how they were achieved.


## Mars News

The most recent news headline and teaser statement from the [NASA Mars News Website](https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest) was scraped using BeautifulSoup.

## Featured Mars Photo

The most recently featured Mars photograph from the [JPL Space Images](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars) website was scraped using BeautifulSoup

## Mars Facts

The Mars Planet Profile table was scraped from the [Space Facts](https://space-facts.com/mars/) website using Pandas.

## Mars Hemispheres

The names and high resolution photographs of four hemispherse of Mars were scraped from the [USGS Astrogeology](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) website. This required visiting and scraping information from four separate URLS, one for each of the hemispheres:
* [Cerberus Hemisphere](https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced)
* [Schiaparelli Hemisphere](https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced)
* [Syrtis Major Hemisphere](https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced)
* [Valles Marineris Hemisphere](https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced)

## Data Collection

The data scraped from the efforts listed above were collected in a single Python dictionary. The code for the scraping activities lives within `scrape_mars.py`. A fully functional, exploratory version of the scraping code is also available in the Jupyter notebook file `mission_to_mars.ipynb`.

## Flask page (app.py)

The Flask page is the launchpad for the rendering of the landing page and execution of the scraping activities. In the absence of any scraping, the landing page will render with the skeleton elements (heading and scrape button). When the scrape button is pressed, the /scrape routing is initiated, which executes the code within `scrape_mars.py`. The scraping activities update the mongo database with new data as appropriate. The user is then redirected back to the landing page, which is updated with and rendered with the newly-scraped information.

 ## Landing Page (index.html)

Flask was used to create a local webserver to host the landing page. A template `index.html` page was created to render the information from Flask, which in turn was obtained from the mongo database that was populated from the webscraping results. The page also contains an interactive scraping button that will launch the web scraping activities and update the page with the most recent news headline and/or featured image, if available. The landing page was structured using Bootstrap.
