# -*- coding: utf-8 -*-

# Project: "Indavelopers"
# Script: handlers.py - Handlers
# App identifier: indavelopers
# URL: www.indavelopers.com
# Author: Marcos Manuel Ortega - Indavelopers
# Version: v4.0 - 12/2015


# -- Imports --
import os
import webapp2
import jinja2

from models import *


# Initialize Jinja2 environment
template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


# -- Handlers --
class MainHandler(webapp2.RequestHandler):
	def render(self, template, params=None):
		if not params:
			params = {}

		t = jinja_env.get_template(template)

		self.response.out.write(t.render(params))


class StaticPage(MainHandler):
	def get(self):
		templates = {'': 'home.html',
		             'contacto': 'contacto.html',
		             'aviso-legal': 'aviso-legal.html',
		             'mapa-web': 'mapa-web.html'}

		page = self.request.path.split('/')[-1]

		try:
			template = templates[page]

		except KeyError:
			template = 'error-404.html'

		self.render(template)


class Projects(MainHandler):
	def get(self):
		projects = Project.get_projects()

		params = {'proyectos': projects}

		self.render('proyectos.html', params)


class News(MainHandler):
	def get(self):
		posts = Post.get_posts(3)

		events = Events.get_events(3)

		params = {'posts': posts,
		          'eventos': events}

		self.render('noticias.html', params)


class Blog(MainHandler):
	def get(self):
		posts = Post.get_posts()

		params = {'posts': posts}

		self.render('blog.html', params)


class PostPage(MainHandler):
	def get(self, title_url):
		post = Post.get_by_title_url(title_url)

		params = {'post': post}

		self.render('post.html', params)


class Events(MainHandler):
	def get(self):
		events = Event.get_events()

		params = {'events': events}

		self.render('events.html', params)


class EventPage(MainHandler):
	def get(self, title_url):
		event = Event.get_by_title_url(title_url)

		params = {'event': event}

		self.render('eventos.html', params)


class AdminHome(MainHandler):
	def get(self):
		self.render('admin-inicio.html')


class AdminProjects(MainHandler):
	def get(self):
		self.render('admin-proyectos.html')


class AdminProjectsEdit(MainHandler):
	def get(self):
		self.render('admin-proyectos-editar.html')


class AdminProjectsDelete(MainHandler):
	def get(self):
		self.render('admin-proyectos-editar.html')


class AdminNews(MainHandler):
	def get(self):
		self.render('admin-noticias.html')


class AdminNewsEdit(MainHandler):
	def get(self):
		self.render('admin-noticias-editar.html')


class AdminNewsDelete(MainHandler):
	def get(self):
		self.render('admin-noticias-editar.html')


class Webmap(MainHandler):
	def get(self):
		self.response.out.write('')


class Error404(MainHandler):
	def get(self):
		self.error(404)

		self.render('error-404.html')
