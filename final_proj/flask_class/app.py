#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 09:13:32 2021

@author: ironhack
"""

from flask import Flask, render_template, request

# We are just telling python that from here donwards we have a flask app 
app = Flask(__name__)


@app.route('/')

def my_function():
    return "Welcome to my personal page, I am Jose"


# we now just need the piece of code that will "run"

@app.route('/student')

def second_funtion():
    return 'I can change pages/routes'


@app.route('/home', methods = ['POST', 'GET'])

def homepage():
    
    if request.method == 'POST':
        
        parameter = request.form['parameter 1']
        
        return render_template('main.html' , x = parameter)
    
    else:
        return render_template('main.html')




if __name__ == "__main__":
    app.run(debug = True, port = 3256)