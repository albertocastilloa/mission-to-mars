from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

#Start an instance of Flash
app = Flask(__name__)

#Connect to Mongo through PyMongo
conn = "mongodb://localhost:27017"

def insert_mars_facts():
    #Create instance of PyMongo
    insert_client = pymongo.MongoClient(conn)

    #Connect to database. Will create if it doesn't exist
    db = insert_client.mars_db

    #Drop collections avaliables
    db.mars_facts.drop()

    #Create collection and insert data from scrape_mars
    db.mars_facts.insert_many([scrape_mars.scrape()])
    
    #Call consult def
    consult_mars_facts()
    
    pass

def consult_mars_facts():
    #Create instance of PyMongo
    consult_client = pymongo.MongoClient(conn)
    #Connect to database.
    db = consult_client.mars_db
    #Get collection.
    mars_facts_dict = db.mars_facts.find_one()
    
    return mars_facts_dict

@app.route("/")
def home():
    #Get mars dict
    mars_data_webpage = consult_mars_facts()
    #Return template and data
    return render_template("index.html", mars_app=mars_data_webpage)

@app.route("/scrape")
def scrape():
    mars_data_webpage = insert_mars_facts()
    #Redirect to index.html
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)