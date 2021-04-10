#Name: Aastha Lamichhane
#file: __init__.py

from flask import Flask, request, render_template
app = Flask(__name__)

from appdir import routes
