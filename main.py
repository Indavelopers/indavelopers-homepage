# -*- coding: utf-8 -*-

# Project: "Indavelopers"
# Script: main.py - App handler mapping
# App identifier: indavelopers
# URL: www.indavelopers.com
# Author: Marcos Manuel Ortega - Indavelopers
# Version: v4.0 - 12/2015


# -- Imports --
import webapp2

from scripts.handlers import *

# -- Handler mapping --
URLS = [('/', StaticPage),
        ('/proyectos', Projects),
        ('/noticias', News),
        ('/noticias/blog', Blog),
        ('/noticias/blog/(.*)', PostPage),
        ('/noticias/eventos', Events),
        ('/noticias/eventos/(.*)', EventPage),
        ('/contacto', StaticPage),
        ('/aviso-legal', StaticPage),
        ('/mapa-web', StaticPage),
        ('/admin', AdminHome),
        ('/admin/proyectos', AdminProjects),
        ('/admin/proyectos/(.*)', AdminProjectsEdit),
        ('/admin/proyectos/(.*)/eliminar', AdminProjectsDelete),
        ('/admin/noticias', AdminNews),
        ('/admin/noticias/(.*)', AdminNewsEdit),
        ('/admin/noticias/(.*)/eliminar', AdminNewsDelete),
        ('/mapaweb', Webmap),
        ('/.*', Error404)]

URLS = [(u[0] + '[/]?', u[1]) for u in URLS]

app = webapp2.WSGIApplication(URLS, debug=True)

# todo home cifras

# todo Mapaweb actualizable
