# -*- coding: utf-8 -*-

# Project: "Indavelopers"
# Script: handlers.py - Handlers
# App identifier: Indavelopers
# URL: www.indavelopers.com
# Author: Marcos Manuel Ortega - Indavelopers
# Version: v5-0 - 03/2018


# -- Imports --
import os
import webapp2
import jinja2

# Initialize Jinja2 environment
template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=False)


# -- Handlers --
class MainHandler(webapp2.RequestHandler):
    def render(self, template, params=None):
        if not params:
            params = {}

        t = jinja_env.get_template(template)

        self.response.out.write(t.render(params))


class HomePage(MainHandler):
    def get(self):
        self.render('home.html')


class LegalPage(MainHandler):
    def get(self):
        self.render('legal.html')


class Error404(MainHandler):
    def get(self):
        self.error(404)

        self.render('error-404.html')
