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
class UsrAPI:
    local_dic = {}
    def addUsr(name, username, password, diction):
        usr_id = len(diction)
        diction[usr_id] = {
            "name" : name,
            "data" : {
                "user" : username,
                "password" : password,
                "bio" : "",
                "bday" : "",
                "interests" : ""
            }
        }
    def addSpecific(id, specific, data, diction):
        if id not in diction: 
            return {"message" : "key not found" }
        else:
            dictionary = diction["data"]
        if specific not in dictionary:
            return {"message" : "specific key in {id} not found" }
        try:
            dictionary[specific] = data
        except Exception as e:
            return {'message' : f"Error found when trying to find specific key {specific}: {e}"}
        

        
    # Update the library, include delete and update
    class _Create(Resource):
        def post(self, name, username, password): # simply creates the endpoint, dne otherwise
            UsrAPI.addUsr(name, username, password, UsrAPI.local_dic)
            pass
    class _Update(Resource):
        def post(self, id, specific, data):
            UsrAPI.addSpecific(id, specific, data)
            pass 
    class _Delete(Resource):
        def get(self, id):
            key = UsrAPI.local_dic.pop(id, None)
            return jsonify({"message" : f"successfully removed {key}"})        
            
    # Add stuff to the library
    class _Read(Resource):
        def get(self):
            return jsonify(UsrAPI.local_dic)     

    # building RESTapi resources/interfaces, these routes are added to Web Server
    api.add_resource(_Create, '/card/create/<string:front>_<string:back>')
    api.add_resource(_Read, '/card/')
    api.add_resource(_Delete, 'card/delete/<int:id>')
    
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
