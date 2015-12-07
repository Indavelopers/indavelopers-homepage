# -*- coding: utf-8 -*-

# Project: "Indavelopers"
# Script: main.py - App handler mapping
# App identifier: indavelopers
# URL: www.indavelopers.com
# Author: Marcos Manuel Ortega - Indavelopers
# Version: v4.0 - 12/2015


# -- Recognize App Engine modules --
import sys

sys.path.append('C:\\Program Files (x86)\\Google\\google_appengine')


# -- Imports --
import webapp2

from scripts.handlers import *


# -- Handler mapping --
URLS = [('/', Home),
        ('/.*', Error404)]

app = webapp2.WSGIApplication(URLS, debug=False)
