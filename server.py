#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# Copyright 2015 Dylan Stankievech
#
# Code modified by Dylan Stankievech for the purposes of CMPUT410 Assignment 4
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


import flask
from flask import Flask, Response, request, redirect, url_for, render_template
import json
app = Flask(__name__)
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    def __init__(self):
        self.clear()
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: appication/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()          

# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data != ''):
        return json.loads(request.data)
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
def hello():
    ''' Return index page '''
    return redirect(url_for('static', filename='index.html'))

@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    ''' Update the specified entity with the supplied data '''
    toUpdate = json.loads(request.data.decode('utf-8'))
    decoded = entity.decode('utf-8')
    myWorld.space[decoded] = toUpdate
    toReturn = json.dumps(toUpdate)
    return Response(toReturn, status=200, mimetype='application/json')

@app.route("/world", methods=['POST','GET'])    
def world():
    ''' Return a json representation of the world '''
    data = json.dumps(myWorld.space)
    response = Response(data, status=200, mimetype='application/json')
    return response

@app.route("/entity/<entity>")    
def get_entity(entity):
    ''' Handle a GET request for specified entity '''
    decoded = entity.decode('utf-8')
    toReturn = {}
    if decoded in myWorld.space:
        toReturn = myWorld.space[decoded]
    data = json.dumps(toReturn)
    response = Response(data, status=200, mimetype='application/json')
    return response

@app.route("/clear", methods=['POST','GET'])
def clear():
    ''' Clear all entities in the world '''
    myWorld.clear()
    return Response(None, status=200)

if __name__ == "__main__":
    app.run()
