from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
import requests  # used for testing 
import random
import wikipediaapi

from model_jokes import *

app_api = Blueprint('api', __name__,
                   url_prefix='/api/wiki')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(app_api)

class WikiAPI:
    # not implemented
    def serialize():
        wiki_wiki = wikipediaapi.Wikipedia('en')

        page_py = wiki_wiki.page('Python_(programming_language)')
        thisdict = {}
        z = 0
        for i in page_py.sections:
            section_id = z
            thisdict["summary"] = page_py.summary[0:60] 
            thisdict["url"] = page_py.fullurl 

        return thisdict
        
    class _Create(Resource):
        def post(self, name):
            pass
            
    # getJokes()
    class _Read(Resource):
        def get(self):
            return jsonify(WikiAPI.serialize())

    # getJoke(id)
    class _ReadID(Resource):
        def get(self, id):
            return jsonify(WikiAPI.serialize())

    # getRandomJoke()
    class _ReadRandom(Resource):
        def get(self):
            return jsonify(WikiAPI.serialize())
    

    # building RESTapi resources/interfaces, these routes are added to Web Server
    api.add_resource(_Create, '/create/<string:name>')
    api.add_resource(_Read, '/')
    api.add_resource(_ReadID, '/<int:id>')
    api.add_resource(_ReadRandom, '/random')
    
if __name__ == "__main__": 
    # server = "http://127.0.0.1:5000" # run local
    server = 'https://flask.nighthawkcodingsociety.com' # run from web
    url = server + "/api/wiki"
    responses = []  # responses list

    # get count of jokes on server
    count_response = requests.get(url+"/count")
    count_json = count_response.json()
    count = count_json['count']

    # update likes/dislikes test sequence
    num = str(random.randint(0, count-1)) # test a random record
    responses.append(
        requests.get(url+"/"+num)  # read joke by id
        ) 
    # obtain a random joke
    responses.append(
        requests.get(url+"/random")  # read a random joke
        ) 

    # cycle through responses
    for response in responses:
        print(response)
        try:
            print(response.json())
        except:
            print("unknown error")