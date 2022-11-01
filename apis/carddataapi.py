from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
import requests  # used for testing 
import random
app_api = Blueprint('api', __name__,
                   url_prefix='/api/cards/')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(app_api)


class CardAPI:
    local_dic = {} # Stores all the users and IDs
    def createuser(user, password, diction):
        user_id = len(diction)
        diction[user_id] = {'user':user, "password":password}
# TODO Figure out how to create a nested dictionary to hold data for the notecards

    class _Create(Resource):
        def post(self, user, password): # simply creates the endpoint, dne otherwise
            CardAPI.createuser(user, password, CardAPI.local_dic)
            pass
# TODO Modify to work with nested dictionaries

    # getJokes()
    class _Read(Resource):
        def get(self):
            return jsonify(CardAPI.local_dic) # init wikipedia by default
# TODO Modift yo send frontend one card at a time.    

    class _GetUserInfo(Resource):
        def get(self):
            return jsonify()
    # getJoke(id)
    #class _ReadWithName(Resource): # read when url have name query satisfied
    #    def get(self, name):
     #       return jsonify()# otherwise check with name

    # getRandomJoke()
    #class _ReadRandom(Resource):
    #    def get(self):
    #        return jsonify() # this exists for some reason
    

    # building RESTapi resources/interfaces, these routes are added to Web Server
    api.add_resource(_Create, '/create/<string:name>')
    api.add_resource(_Read, '/')
    api.add_resource(_GetUserInfo,'/user')
    
if __name__ == "__main__": # THIS ONLY RUNS IF YOU RUN THE FILE, NOT IF YOU OPEN IN A TAB. ONLY USE FOR DEBUGGING
    # server = "http://127.0.0.1:5000" # run local
    server = 'https://flask.nighthawkcodingsociety.com' # run from web
    url = server + "/api/cards"
    responses = []  # responses list

    # get count of jokes on server
    count_response = requests.get(url+"/count")
    count_json = count_response.json()
    count = count_json['count']

    # update likes/dislikes test sequence
    #num = str(random.randint(0, count-1)) # test a random record
    #responses.append(
    #    requests.get(url+"/"+num)  # read joke by id
    #    ) 

    # obtain a random joke
    #responses.append(
    #    requests.get(url+"/random")  # read a random joke
    #    ) 

    # cycle through responses
    #for response in responses:
    #    print(response)
    #    try:
    #        print(response.json())
    #    except:
    #        print("unknown error")
