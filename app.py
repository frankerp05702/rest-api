import uuid
from flask import Flask, request
from db import items, stores

app = Flask(__name__)

@app.get("/store") #http:127.0.0.1:5000
def get_stores():
    return {"stores": list(stores.values())}

@app.get("/storeid") #http:127.0.0.1:5000
def get_stores_ids():
    return {"stores_ids": list(stores.keys())}

@app.get("/item") #http:127.0.0.1:5000
def get_items():
    return {"items": list(items.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        return { "message": "Bad request. Ensure 'name' is included in the JSON payload" }, 400
    for store in stores.values():
        if store["name"]==store_data["name"]:
            return { "message": "Store already exists" }, 400
    store_id = uuid.uuid4().hex
    store = { **store_data, "id":store_id }
    stores[store_id] = store
    return store, 201

@app.post("/item")
def create_item():
    item_data = request.get_json()
    # Here not only validate data exists,
    # Also what type of data. Price should be a float, for example
    if(
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        return { "message": "Bad request. Ensure 'price', 'store_id' and 'name' are included in the JSON payload" }, 400
    # Ensure that same item is not added twice
    for item in items.values():
        if(
            item["name"]==item_data["name"]
            or item["store_id"]==item_data["store_id"]
        ):
            return { "message": "Item already exists" }, 400
        
    if item_data["store_id"] not in stores:
        return { "message": "Store not found" }, 404
    
    item_id = uuid.uuid4().hex
    item = { **item_data, "id":item_id }
    items[item_id] = item

    return item, 201

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    # Here not only validate data exists,
    # Also what type of data. Price should be a float, for example
    if(
        "price" not in item_data
        and "name" not in item_data
    ):
        return { "message": "Bad request. Ensure 'price' and 'name' are included in the JSON payload" }, 400
    
    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        return { "message":"Item not found" }, 404

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except:
        return { "message":"Item not found" }, 404
    
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return { "message":"Item deleted" }, 201
    except KeyError:
        return { "message":"Item not found" }, 404

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id], 201
    except KeyError:
        return { "message": "Store not found" }, 404

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return { "message":"store deleted" }, 201
    except:
        return { "message":"store not found" }, 404

@app.get("/store/<string:store_id>/item")
def get_store_items(store_id):
    res_items = []
    if store_id not in stores.keys():
        return { "message": "Store not found" }, 404
    for item in items.values():
        if item["store_id"]==store_id:
            res_items.append(item)
    return { "items": res_items }, 201