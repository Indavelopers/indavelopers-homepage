# -*- coding: utf-8 -*-

# Project: "Indavelopers"
# Script: handlers.py - Handlers
# App identifier: indavelopers
# URL: www.indavelopers.com
# Author: Marcos Manuel Ortega - Indavelopers
# Version: v4.0 - 12/2015


# -- Recognize App Engine modules --
import sys

sys.path.append('C:\\Program Files (x86)\\Google\\google_appengine')


# -- Imports --
import os
import webapp2
import jinja2


# Initialize Jinja2 environment
template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


# -- Handlers --
class MainHandler(webapp2.RequestHandler):
    def render(self, template):
        t = jinja_env.get_template(template)

        self.response.out.write(t.render())


class StaticPage(MainHandler):
    def get(self):
        templates = {'': 'home.html',
                     'proyectos': 'proyectos.html',
                     'contacto': 'contacto.html',
                     'aviso-legal': 'aviso-legal.html',
                     'mapa-web': 'mapa-web.html'}

        page = self.request.path.split('/')[-1]

        template = templates[page]

        self.render(template)


class Proyectos(MainHandler):
    def get(self):
        self.render('proyectos.html')


class Noticias(MainHandler):
    def get(self):
        self.render('noticias.html')


class Blog(MainHandler):
    def get(self):
        self.render('blog.html')


class PaginaPost(MainHandler):
    def get(self):
        self.render('post.html')


class Eventos(MainHandler):
    def get(self):
        self.render('eventos.html')


class PaginaEvento(MainHandler):
    def get(self):
        self.render('evento.html')


class AdminInicio(MainHandler):
    def get(self):
        self.render('admin-inicio.html')


class AdminProyectos(MainHandler):
    def get(self):
        self.render('admin-proyectos.html')


class AdminNoticias(MainHandler):
    def get(self):
        self.render('admin-noticias.html')


class Error404(MainHandler):
    def get(self):
        self.error(404)

        self.render('error-404.html')
