# app.py for Web Scraping Challenege
# Written by Jason Gabunilas

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection.
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find (or create) the mars collection from the mongo database
    mars_dict = mongo.db.mars.find_one()

    # Return template and data. Set the variable mars equal to the data from the database
    return render_template("index.html", mars=mars_dict)

# Route that will trigger the Mars scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function to obtain the Mars data
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True, passing in mars_data dictionary
    mongo.db.mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)