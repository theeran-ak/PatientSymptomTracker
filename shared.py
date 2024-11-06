'''----------MODULE CONTAINING THE MAIN MODULES AND FLASK OBJECT FOR THE FLASK APPLICATION-----------'''
from flask import Flask, render_template, request, url_for, redirect
from flask_cors import CORS
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import joblib
import json
import pymysql
app = Flask(__name__)
symptom_name="common"
#Load all possible symptoms
with open("static/symptom.json", "r") as json_file:
    symptom_type = json.load(json_file)
symptoms = symptom_type["Symptom"]