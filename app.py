import os

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.config["MONGO_URI"] = "mongodb://localhost:27017/compra"
    mongo = PyMongo(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello

    def hello():
        return 'Hello, World2!'

    @app.route('/lista', methods=['GET', 'POST','PUT'])
    def showList():
        if request.method == 'GET':
            # result = mongo.db.lista.find_one({'nombre':'patatas'},{'_id':0})
            result = mongo.db.lista.find({},{'_id':0})
            arrayItems = []
            for item in result:
                arrayItems.append(item)
            return jsonify(arrayItems)
        if request.method == 'POST':

            return "OK POST"
        return "Something's wrong"

    @app.route('/articulos/remove', methods =['POST'])
    def removeArticle():
        if request.method == 'POST':
            #do something
            mongo.db.articulos.delete_one({'_id':ObjectId(request.get_json()['_id'])})
            return 'OK', 200

    @app.route('/articulos', methods=['GET', 'POST','PUT','DELETE'])
    def showArticles():
        if request.method == 'GET':           
            result = mongo.db.articulos.find({})            
            arrayItems = []
            for item in result:
                item['_id'] = str(item['_id'])
                arrayItems.append(item)
                print(item)
            return jsonify(arrayItems)
        if request.method == 'POST':
            print(request.get_json())
            mongo.db.articulos.insert_one(request.get_json())
            return 'ok', 200
        return "Something's wrong"
    
    @app.route('/articulos/patch', methods=['PATCH'])
    def updateQuantity():
        if request.method == 'PATCH':
            mongo.db.articulos.update_one({'_id':ObjectId(request.get_json()['_id'])},\
                                          {"$set": {"quantity":request.get_json()['quantity']}})
        return 'OK', 200    
    return app