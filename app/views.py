from flask import Flask, request, flash, render_template
from app import app
import re
import sqlite3
import sys

def init_db():
    ''' Initializes the database connection for the LoL function '''
    conn = sqlite3.connect('champs.db')
    conn.text_factory = str
    c = conn.cursor()
    return c

def init_dota_db():
    ''' Initializes the database connection for the DOTA2 function '''
	conn = sqlite3.connect('dota.db')
	conn.text_factory = str
	c = conn.cursor()
	return c

@app.route('/')
@app.route('/index')
def index():
    db = init_db() # initialize the database

    cur = db.execute("SELECT DISTINCT name from HeroCounters") # get the list of champions
    heroes = cur.fetchall()
    heroes_list = [] # initialize the list so we can pass the list to the view
    heroes_list.append("---")
    for eachHero in heroes:
        heroes_list.append(str(eachHero[0])) # generate the list
    return render_template("index.html",heroes=heroes_list)  # push the list to the view


@app.route('/dota')
def dota():
	db = init_dota_db() # initialize the database
	
	cur = db.execute("SELECT DISTINCT name from HeroCounters") # get the list of heroes
	heroes = cur.fetchall()
	heroes_list = [] # initialize the list so we can pass the list to the view
	heroes_list.append("---")
	for eachHero in heroes:
		heroes_list.append(str(eachHero[0])) # generate the list
	return render_template("indexDOTA.html",heroes=heroes_list) # push the list to the view

@app.route('/_find', methods=["POST"])
def find_champs():
    ''' Takes the input values from the main page, and finds common counters '''

    a = request.form['ally1']
    b = request.form['ally2']
    c = request.form['ally3']
    d = request.form['ally4']
    e = request.form['ally5']

    # initialize all our variables
    champList = [a,b,c,d,e]
    master_dict = {}
    outList = []
    namedict = {}

    # database connection
    db = init_db()

    for eachChamp in champList:
        # cur = db.execute('SELECT * FROM HeroCounters WHERE name = "%s"' % eachChamp)
        # for eachEntry in cur.fetchall():
        cmd = 'SELECT * FROM HeroCounters WHERE name=?'
        for eachEntry in db.execute(cmd, (eachChamp,)):
            countered_by_name = eachEntry[1]
            if str(countered_by_name) in master_dict:
                got_this = master_dict[str(countered_by_name)] #got_this = num_times
                got_this += 1
                master_dict[str(countered_by_name)] = got_this
            else:
                master_dict[str(countered_by_name)] = 1

            #sets the list of counters
            if countered_by_name in namedict:
                namedict[countered_by_name] = namedict[countered_by_name] + ", " + eachChamp
            else:
                namedict[countered_by_name] = eachChamp

    for w in sorted(master_dict, key=master_dict.get, reverse=True):
      if master_dict[w] > 1:
        outList.append({'num': str(w), 'name': str(master_dict[w]), 'whichchamps': str(namedict[w])})

    

    return render_template("champs.html",counters=outList)

@app.route('/_findDOTA', methods=["POST"])
def find_champs_dota():
	a = request.form['ally1']
	b = request.form['ally2']
	c = request.form['ally3']
	d = request.form['ally4']
	e = request.form['ally5']

	champList = [a,b,c,d,e]
	master_dict = {}
	outList = []
	namedict = {}

	db = init_dota_db()

	for eachChamp in champList:
	    # cur = db.execute('SELECT * FROM HeroCounters WHERE name = "%s"' % eachChamp)
	    # for eachEntry in cur.fetchall():
	    cmd = 'SELECT * FROM HeroCounters WHERE name=?'
	    for eachEntry in db.execute(cmd, (eachChamp,)):
	        countered_by_name = eachEntry[1]
	        if str(countered_by_name) in master_dict:
	            got_this = master_dict[str(countered_by_name)] #got_this = num_times
	            got_this += 1
	            master_dict[str(countered_by_name)] = got_this
	        else:
	            master_dict[str(countered_by_name)] = 1

	        #sets the list of counters
	        if countered_by_name in namedict:
	            namedict[countered_by_name] = namedict[countered_by_name] + ", " + eachChamp
	        else:
	            namedict[countered_by_name] = eachChamp

	for w in sorted(master_dict, key=master_dict.get, reverse=True):
	  if master_dict[w] > 1:
	    outList.append({'num': str(w), 'name': str(master_dict[w]), 'whichchamps': str(namedict[w])})



	return render_template("champs.html",counters=outList)
