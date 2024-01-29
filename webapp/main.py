# -*- coding: utf-8 -*-

# Project: "Indavelopers"
# Script: main.py - App handler mapping
# App identifier: Indavelopers
# URL: www.indavelopers.com
# Author: Marcos Manuel Ortega - Indavelopers
# Version: v6 - 01/2024


from flask import Flask, render_template
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='b0b8a4ad4aad160f9095453cf6fa4aeb9c1a3da7aa6c53210e9e74223eddb921')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/aviso-legal')
def legal():
    return render_template('legal.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error-404.html'), 404


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    
    return render_template('error-500.html'), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)
