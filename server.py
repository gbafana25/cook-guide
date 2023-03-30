#!/usr/bin/python3

from flask import Flask, request
import requests


app = Flask(__name__)

@app.route("/test", methods=["GET"])
def testPoint():
	return "test data"


if __name__ == "__main__":
	app.run()


