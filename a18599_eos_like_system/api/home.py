from flask import Blueprint

from flask import send_from_directory
from flask import request
from flask import url_for
from flask import redirect, session
from flask import Blueprint, render_template as rt
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, Response
from flask import jsonify
from flask_cors import CORS


api = Blueprint('api', __name__)

@api.route('/', defaults={'page': 'index'})
def show(page):
    return "Home"