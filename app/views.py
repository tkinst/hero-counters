from flask import Flask, request, flash, render_template
from app import app
import re
import sqlite3
import sys

def init_db():
    conn = sqlite3.connect('champs.db')
    conn.text_factory = str
    c = conn.cursor()
    return c

def index2():
    user = { 'nickname': 'Miguel' } #fake user
    posts = [ # fake array of posts
        { 
            'author': { 'nickname': 'John' }, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': { 'nickname': 'Susan' }, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)


@app.route('/')
@app.route('/index')
def index():
    db = init_db()

    cur = db.execute("SELECT DISTINCT name from HeroCounters")
    heroes = cur.fetchall()
    heroes_list = []
    heroes_list.append("---")
    for eachHero in heroes:
        heroes_list.append(str(eachHero[0]))
    return render_template("index.html",heroes=heroes_list)


@app.route('/_find', methods=["POST"])
def find_champs():
    a = request.form['ally1']
    b = request.form['ally2']
    c = request.form['ally3']
    d = request.form['ally4']
    e = request.form['ally5']

    champList = [a,b,c,d,e]
    master_dict = {}
    outList = []
    namedict = {}

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
