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
URLS = [('/', StaticPage),
        ('/proyectos', Proyectos),
        ('/noticias', Noticias),
        ('/noticias/blog', Blog),
        ('/noticias/blog/(.*)', PaginaPost),
        ('/noticias/eventos', Eventos),
        ('/noticias/eventos/(.*)', PaginaEvento),
        ('/contacto', StaticPage),
        ('/aviso-legal', StaticPage),
        ('/mapa-web', StaticPage),
        ('/admin', AdminInicio),
        ('/admin/proyectos', AdminProyectos),
        ('/admin/noticias', AdminNoticias),
        ('/.*', Error404)]

URLS = [(u[0] + '[/]?', u[1]) for u in URLS]

app = webapp2.WSGIApplication(URLS, debug=True)

# todo home cifras
# todo todas paginas description tag

# todo Admin editar entrada
# todo Admin eliminar entrada
# todo Crear entrada/evento/proyecto, actualizar mapa web (página y txt)

# todo Avisador de servicio no disponible

