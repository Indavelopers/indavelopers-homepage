# -*- coding: utf-8 -*-

# Project: "Indavelopers"
# Script: main.py - App handler mapping
# App identifier: Indavelopers
# URL: www.indavelopers.com
# Author: Marcos Manuel Ortega - Indavelopers
# Version: v4.0 - 12/2015


# -- Imports --
import webapp2

from scripts.handlers import *

# -- Handler mapping --
URLS = [('/', StaticPage),
        ('/proyectos', ProjectsPage),
        ('/proyectos/(.+)', ProjectPage),
        ('/blog', Blog),
        ('/blog/(.+)', PostPage),
        ('/eventos', Events),
        ('/eventos/(.+)', EventPage),
        ('/contacto', StaticPage),
        ('/aviso-legal', StaticPage),
        ('/mapa-web', StaticPage),
        ('/autograder/(.+)', AutograderPage),
        ('/admin', AdminHome),
        ('/admin/proyectos', AdminProjects),
        ('/admin/proyectos/(\d+|nuevo)', AdminProjectsEdit),
        ('/admin/proyectos/(\d+)/eliminar', AdminProjectsDelete),
        ('/admin/noticias', AdminNews),
        ('/admin/noticias/(blog|eventos)/(\d+|nuevo)', AdminNewsEdit),
        ('/admin/noticias/(blog|eventos)/(\d+)/eliminar', AdminNewsDelete),
        ('/webmap', Webmap),
        ('/.*', Error404)]

URLS = [(u[0] + '[/]?', u[1]) for u in URLS]

app = webapp2.WSGIApplication(URLS, debug=True)
