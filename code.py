#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import MySQLdb
import json
import sys
import urllib

from flask import Flask, g, jsonify, make_response
from MySQLdb.cursors import DictCursor


application = Flask(__name__)

# MySQL settings
HOST = ""
DBNAME = ""
USER = ""
PASS = ""


def connect_db():
    return MySQLdb.connect(host=HOST, db=DBNAME, user=USER, passwd=PASS)

@application.before_request
def before_request():
    g.db = connect_db()

@application.teardown_request
def teardown_request(exception):
    g.db.close()

@application.route("/")
def index():
    return "Zip code API"

@application.route("/code/<zipcode>")
def search_place(zipcode):
    cursor = g.db.cursor(DictCursor)
    cursor.execute("SELECT * FROM zipcode WHERE zip_code = %s", (zipcode,))
    items = cursor.fetchall()

    response = make_response(json.dumps(items))
    response.headers["Content-Type"] = "application/json"

    return response

@application.route("/place/<placename>")
def search_code(placename):
    cursor = g.db.cursor(DictCursor)
    cursor.execute("SELECT zip_code FROM zipcode WHERE CONCAT(prefecture, city, town) LIKE '%%%s%%' ORDER BY zip_code ASC" % \
                   MySQLdb.escape_string(urllib.unquote(placename)))
    items = cursor.fetchall()

    response = make_response(json.dumps(items))
    response.headers["Content-type"] = "application/json"

    return response

if __name__ == "__main__":
    application.run()
