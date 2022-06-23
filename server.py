import json 
from flask import Flask, abort, request
from autobio import me
from mock_data import catalog
from config import db
from bson import ObjectId



app = Flask('whoknows')

@app.route("/", methods=['GET'])
def home():
    return "WhoKnows?"

@app.route("/about")
def about():
   
    
    return me["first"] + " " + me["last"]


@app.route("/myaddress")
def address():
    return f'Address:  {me["address"]["street"]} {me["address"]["number"]} '



################ API ENDPOINTS ############

#  Postman --> test endpoints of REST API's


@app.route("/api/catalog", methods=["POST"])
def get_catalog():
    results = []
    cursor = db.products.find({})  #get all data from the database
    
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)
    

# POST method to create new products

@app.route("/api/catalog", methods=["POST"])
def save_product():

    try:

        product = request.get_json()
        errors = ""


        if not "title" in product or len(product["title"]) < 5:
                error = "Title is required; must be at least 5 characters"

        if not "image" in product:
                errors += ", Image is required"

        if not "price" in product or product["price"] < 1:
                errors += ", Price is required"

        if errors:
            return abort(400, errors)


        db.products.insert_one(product)

        product["_id"] = str(product["_id"])    

        return json.dumps(product)

    except Exception as ex:
        return abort (500, F"Unexpected error: {ex}")



@app.route("/api/catalog/inventory", methods=["Get"])
def get_inventory():

    cursor = db.products.find({})
        
    inventory = 0

    for prod in cursor:
        num_items += 1
        

        return json.dumps(inventory)


@app.route("/api/product/<id>", methods=["Get"])
def get_product(id):    

    try:
        if not ObjectId.is_valid(id):
            return abort(400,"Invalid id")

        product = db.products.find_one({"_id": ObjectId(id)})

        if not product:
            return abort(404, "Product not found")

        product["_id"] = str(product["_id"])
        return json.dumps(product)
    
    except: 
        return abort(500, "Unexpected error")


@app.get("/api/catalog/total")
def get_total():

    total = 0
    cursor = db.products.find({})
    for prod in cursor: 
        total += prod["price"]

    return json.dumps(total)


@app.get("/api/catalog/<category>")
def products_by_category(category):

    results = []
    cursor = db.products.find({"category": category})
  
    for prod in cursor:
       prod["_id"] = str(prod["_id"])
       results.append(prod)


    return json.dumps(results)

@app.get("/api/categories")
def get_unique_categories():
    cursor = db.products.find({})
    results = []
    for prod in cursor:
        cat = prod["category"]
        if not cat in results:
            results.append(cat)

    return json.dumps(results) 


app.get("/api/product/cheapest")
def get_cheapest_product():
    cursor = db.products.find({})
    solution = cursor[0]
    for prod in cursor:
        if prod["price"] < solution["price"]:
            solution = prod

    solution["_id"] = str(solution["_id"])
    return json.dumps(solution)        



@app.get("/api/exercise1")
def get_exe1():
    nums = [123,123,654,124,8865,532,4768,8476,45762,345,-1,234,0,-12,-456,-123,-865,532,4768]

    # print the lowest number

    # count and print how many numbers are lowe than 500

    # sum and print all the negatives


    # return the sum of numbers except negatives




##########COUPON CODES

@app.route("/api/coupons", methods=["GET"])
def get_all_coupons():
    cursor = db.coupons.find({})
    results = []
    for cc in cursor:
        cc["_id"] = str(cc["_id"])
        results.append(cc)

    return json.dumps(results)
    

@app.route("/api/coupons", methods=["post"])
def save_coupon():
    coupon = request.get_json()
    db.coupons.insert_one(coupon)

    #validations

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)



app.run(debug=True)