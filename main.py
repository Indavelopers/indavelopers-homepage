# -*- coding: utf-8 -*-

# Project: "Indavelopers"
# Script: main.py - App handler mapping
# App identifier: Indavelopers
# URL: www.indavelopers.com
# Author: Marcos Manuel Ortega - Indavelopers
# Version: v5-2 - 03/2018


# -- Imports --
import webapp2

from scripts.handlers import *

# -- Handler mapping --
URLS = [('/', HomePage),
        ('/aviso-legal', LegalPage),
        ('/.*', Error404)]
URLS = [(u[0] + '[/]?', u[1]) for u in URLS]

app = webapp2.WSGIApplication(URLS, debug=True)
