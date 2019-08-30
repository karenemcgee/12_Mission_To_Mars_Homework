from flask import Flask, render_template
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection

conn = 'mongodb+srv://karen:CtfoeB709bm@firstcluster-pesig.mongodb.net/test'
client = pymongo.MongoClient(conn)

mongo = client.mars

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping was a stellar success!"


if __name__ == "__main__":
    app.run()