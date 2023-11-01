import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

from schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id], 201
        except KeyError:
            abort( 404, message="Store not found" )

    def delete(self, store_id):
        try:
            del stores[store_id]
            return { "message":"store deleted" }, 201
        except:
            abort( 404, message="Store not found" )

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        try:
            store = stores[store_id]
            store |= store_data
            return store
        except KeyError:
            abort( 404, message="Store not found" )

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return {"stores": list(stores.values())}

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store["name"]==store_data["name"]:
                abort( 400, message="Store already exists" )
        store_id = uuid.uuid4().hex
        store = { **store_data, "id":store_id }
        stores[store_id] = store
        return store, 201