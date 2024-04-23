#
# Setup
#

# Imports
from flask import Flask, request, Response
from waitress import serve
from pymongo import MongoClient
from bson import json_util, ObjectId
from os import environ
from urllib import parse

# Environment vars
dbhost = environ['HOST']
dbuser = environ['USER']
dbpass = environ['PASS']
dbname = environ['DATABASE']

# Database setup
mongodb_client = MongoClient('mongodb://' + parse.quote_plus(dbuser) + ':' + parse.quote_plus(dbpass) + '@' + parse.quote_plus(dbhost))
database = mongodb_client[dbname]

# Flask setup
app = Flask(__name__)


#
# Routes
#

# Get entries
@app.route('/<collection>',methods = ['GET'])
def get_many(collection):
    try:
        number = request.args.get('number', default = 100, type = int)
        skip = request.args.get('skip', default = 0, type = int)
        filter = request.args.get('filter', default = "{}", type = str)
        data = json_util.dumps(database[collection].find(limit=number, skip=skip, filter=json_util.loads(filter)))
        return Response(data, mimetype='application/json', status=200)
    except Exception as e:
        app.logger.error(e)
        return Response('Failed. Check collection and filter are valid. Check database logs for errors.\n' + str(e) + '\n', mimetype='text/plain', status=500)

@app.route('/<collection>/<id>',methods = ['GET'])
def get_one(collection, id):
    try:
        data = json_util.dumps(database[collection].find_one({'_id': ObjectId(id)}))
        return Response(data, mimetype='application/json', status=200)
    except Exception as e:
        app.logger.error(e)
        return Response('Failed. Check collection and id are valid. Check database logs for errors.\n' + str(e) + '\n', mimetype='text/plain', status=500)

# Update entries
@app.route('/<collection>',methods = ['PATCH'])
def update_many(collection):
    try:
        data = json_util.loads(request.data)
        filter = request.args.get('filter', default = "{}", type = str)
        result = database[collection].update_many(json_util.loads(filter), data)
        res = json_util.dumps({"matched": result.matched_count, "modified": result.modified_count})
        return Response(res, mimetype='application/json', status=200)
    except Exception as e:
        app.logger.error(e)
        return Response('Failed. Check json body, collection and filter are valid. Check database logs for errors.\n' + str(e) + '\n', mimetype='text/plain', status=500)

@app.route('/<collection>/<id>',methods = ['PATCH'])
def update_one(collection, id):
    try:
        data = json_util.loads(request.data)
        result = database[collection].update_one({'_id': ObjectId(id)}, data)
        res = json_util.dumps({'_id': ObjectId(id)})
        return Response(res, mimetype='application/json', status=200)
    except Exception as e:
        app.logger.error(e)
        return Response('Failed. Check json body, collection and id are valid. Check database logs for errors.\n' + str(e) + '\n', mimetype='text/plain', status=500)

# Replace entry
@app.route('/<collection>/<id>',methods = ['PUT'])
def replace_one(collection, id):
    try:
        data = json_util.loads(request.data)
        result = database[collection].replace_one({'_id': ObjectId(id)}, data)
        res = json_util.dumps({"matched": result.matched_count, "modified": result.modified_count})
        return Response(res, mimetype='application/json', status=200)
    except Exception as e:
        app.logger.error(e)
        return Response('Failed. Check json body, collection and id are valid. Check database logs for errors.\n' + str(e) + '\n', mimetype='text/plain', status=500)

# Delete entries
@app.route('/<collection>',methods = ['DELETE'])
def delete_many(collection):
    try:
        filter = request.args.get('filter', default = "{}", type = str)
        result = database[collection].delete_many(json_util.loads(filter))
        res = json_util.dumps({"deleted": result.deleted_count})
        return Response(res, mimetype='application/json', status=200)
    except Exception as e:
        app.logger.error(e)
        return Response('Failed. Check collection and filter are valid. Check database logs for errors.\n' + str(e) + '\n', mimetype='text/plain', status=500)

@app.route('/<collection>/<id>',methods = ['DELETE'])
def delete_one(collection, id):
    try:
        result = database[collection].delete_one({'_id': ObjectId(id)})
        res = json_util.dumps({'_id': ObjectId(id)})
        return Response(res, mimetype='application/json', status=200)
    except Exception as e:
        app.logger.error(e)
        return Response('Failed. Check collection and id are valid. Check database logs for errors.\n' + str(e) + '\n', mimetype='text/plain', status=500)

# Add entries
@app.route('/<collection>',methods = ['POST'])
def add(collection):
    try:
        data = json_util.loads(request.data)
        result = database[collection].insert_one(data)
        res = json_util.dumps({"_id": ObjectId(result.inserted_id)})
        return Response(res, mimetype='application/json', status=200)
    except Exception as e:
        app.logger.error(e)
        return Response('Failed. Check body json body and collection are valid. Check database logs for errors.\n' + str(e) + '\n', mimetype='text/plain', status=500)

# Fallback (help)
@app.errorhandler(404)
def page_not_found(error):
    return Response('Usage:\n' \
                    '  GET    /<collection>?number=<n>&skip=<s>&filter=<f> => get n entries in collection that match f (skip s)\n' \
                    '  GET    /<collection>/<id>                           => get entry in collection with id\n' \
                    '  POST   /<collection> [json]                         => add an entry to collection using json\n' \
                    '  PATCH  /<collection>?filter=<f> [json]              => update the entries in collection that match f using json\n' \
                    '  PATCH  /<collection>/<id> [json]                    => update the entry in collection with id using json\n' \
                    '  PUT    /<collection>/<id> [json]                    => replace the entry in collection with id using json\n' \
                    '  DELETE /<collection>?filter=<f>                     => delete all entries in collection that match f\n' \
                    '  DELETE /<collection>/<id>                           => delete the entry in collection with id\n' \
                    '', mimetype='text/plain', status=404)


#
# Start
#

serve(app, host='0.0.0.0', port=8000)
