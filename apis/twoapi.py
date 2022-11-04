from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
import requests  # used for testing 
import random
import wikipediaapi
app_api = Blueprint('api', __name__,
                   url_prefix='/api/')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(app_api)

'''
I combined both in order to support both endpoints on the same area. may allow us to pivot should it be necessary
basically tricks the server into running both ends
'''
class CardAPI:
    def serialize(name):
        wiki_wiki = wikipediaapi.Wikipedia('en') # make a wikipedia api object

        page_py = wiki_wiki.page(name) # init to wikipedia by default for default page, otherwise check name
        thisdict = {} # create a dictionary
        thisdict["url"] = page_py.fullurl 
        thisdict["summary"] = page_py.summary
        for i in page_py.sections:
            thisdict[i.title] = i.text
              # init values
            

        return thisdict

    local_dic = {} # Stores all the users and IDs
    def card(front, back, diction):
        user_id = len(diction)
        diction[user_id] = {'title':front, "substance":back}
    def delete_all(query):
        if query == "true":
            local_dic = {}
            return {"message" : "operation successful"}
        else:
            return {"message" : "operation failure"}

    class _Create(Resource):
        def post(self, front, back): # simply creates the endpoint, dne otherwise
            CardAPI.card(front, back, CardAPI.local_dic)
            pass
            
    # getJokes()
    class _Read(Resource):
        def get(self):
            return jsonify(CardAPI.local_dic) # init wikipedia by default

    class _WikiRead(Resource):
        def get(self):
            return jsonify(CardAPI.serialize('wikipedia')) # init wikipedia by default

    # getJoke(id)
    class _ReadWithName(Resource): # read when url have name query satisfied
        def get(self, name):
            return jsonify(CardAPI.serialize(name))# otherwise check with name
    class _Delete(Resource):
        def get(self, query):
            return jsonify(CardAPI.delete_all(query))

    
    # getJoke(id)
   # class _ReadWithName(Resource): # read when url have name query satisfied
    #    def get(self, name):
     #       return jsonify()# otherwise check with name

    # getRandomJoke()
    #class _ReadRandom(Resource):
     #   def get(self):
      #      return jsonify() # this exists for some reason
    

    # building RESTapi resources/interfaces, these routes are added to Web Server
    api.add_resource(_Create, '/card/create/<string:front>_<string:back>')
    api.add_resource(_Read, '/card/')
    api.add_resource(_WikiRead, '/wiki/')
    api.add_resource(_ReadWithName, '/wiki/<string:name>')
    
if __name__ == "__main__": # THIS ONLY RUNS IF YOU RUN THE FILE, NOT IF YOU OPEN IN A TAB. ONLY USE FOR DEBUGGING
    # server = "http://127.0.0.1:5000" # run local
    server = 'https://flask.nighthawkcodingsociety.com' # run from web
    url = server + "/api/auth"
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
