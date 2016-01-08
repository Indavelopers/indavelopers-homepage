# -*- coding: utf-8 -*-

# Project: "Indavelopers"
# Script: handlers.py - Handlers
# App identifier: Indavelopers
# URL: www.indavelopers.com
# Author: Marcos Manuel Ortega - Indavelopers
# Version: v4.0 - 12/2015


# -- Imports --
import os
import webapp2
import jinja2
from models import *
from globals import *


# Initialize Jinja2 environment
template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


# -- Handlers --
class MainHandler(webapp2.RequestHandler):
	@staticmethod
	def flush_mc(keys=None):
		if not (type(keys) is str or type(keys) is list or keys is None):
			raise TypeError

		max_retries = 50

		if type(keys) is str:
			for _ in xrange(max_retries):
				if mc.delete(keys):
					break

			else:
				return False

		elif type(keys) is list:
			for _ in xrange(max_retries):
				if mc.delete_multi(keys):
					break

			else:
				return False
		else:
			for _ in xrange(max_retries):
				if mc.flush_all():
					break

			else:
				return False

		return True

	def render(self, template, params=None):
		if not params:
			params = {}

		t = jinja_env.get_template(template)

		self.response.out.write(t.render(params))


class StaticPage(MainHandler):
	def get(self):
		templates = {'': 'inicio.html',
		             'contacto': 'contacto.html',
		             'aviso-legal': 'aviso-legal.html',
		             'mapa-web': 'mapa-web.html'}

		page = self.request.path.split('/')[-1]

		try:
			template = templates[page]

		except KeyError:
			template = 'error-404.html'

		self.render(template)


class ProjectsPage(MainHandler):
	def get(self):
		projects = Project.get_projects()

		params = {'projects': projects}

		self.render('proyectos.html', params)


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

		self.render('eventos.html', params)


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
		projects = Project.get_projects()

		params = {'proyectos': projects}

		self.render('admin-proyectos.html', params)


class AdminProjectsEdit(MainHandler):
	def get(self, id_):
		new_project = id_ == 'nuevo'

		type_ = self.request.get('tipo')

		params = {}

		if not new_project:
			project = Project.get_by_id_(id_)

			if project:
				params['title'] = project.title
				params['date'] = project.date
				params['description'] = html_to_markdown(project.description)
				params['type'] = CONTENT_TYPES[type_]

			else:
				params['error'] = 'Proyecto no encontrado.'

		self.render('admin-proyectos-editar.html', params)

	def post(self, id_):
		title = self.request.get('title')
		description = self.request.get('description')
		type_ = self.request.get('tipo')

		new_project = id_ == 'nuevo'

		error = ''

		if not new_project:
			project = Project.get_by_id_(id_)

			if not project:
				error = 'Proyecto no encontrado.'

		if not error:
			project_params = {'instance': 'nuevo' if new_project else project,
			                  'type': type_,
			                  'title': title,
			                  'description': description}

			res = Project.validate_params(project_params)

			if res:
				Project.edit_instance(project_params)

				self.flush_mc()

			else:
				error = res

		if error:
			params = {'error': error,
			          'title': title,
			          'description': description,
			          'type': CONTENT_TYPES[type_]}

			self.render('admin-proyectos-editar.html', params)

		else:
			self.redirect('/admin/proyectos')


class AdminProjectsDelete(MainHandler):
	def get(self, id_):
		project = Project.get_by_id_(id_)

		type_ = self.request.get('tipo')

		params = {}

		if id_ != 'nuevo' and project:
			params['project'] = project
			params['type'] = CONTENT_TYPES[type_]

		else:
			params['error'] = 'Proyecto no encontrado.'

		self.render('admin-proyectos-eliminar.html', params)

	def post(self, id_):
		project = Project.get_by_id_(id_)

		params = {}

		if id_ != 'nuevo' and project:
			project.delete_entity()

		else:
			params['error'] = 'Proyecto no encontrado.'

		self.redirect('/admin/projects')


class AdminNews(MainHandler):
	def get(self):
		posts = Post.get_posts()
		events = Events.get_events()

		params = {'posts': posts,
		          'eventos': events}

		self.render('admin-noticias.html', params)


class AdminNewsEdit(MainHandler):
	def get(self, type_, id_):
		if type_ == 'blog':
			class_ = Blog
		else:
			class_ = Event

		new_news = id_ == 'nuevo'

		params = {}

		if not new_news:
			news = class_.get_by_id_(id_)

			if news:
				params['title'] = news.title
				params['date'] = news.date
				params['description'] = html_to_markdown(news.description)
				params['type'] = CONTENT_TYPES[type_]

			else:
				params['error'] = 'Noticia no encontrado.'

		self.render('admin-noticias-editar.html', params)

	def post(self, type_, id_):
		title = self.request.get('title')
		description = self.request.get('description')

		if type_ == 'blog':
			class_ = Blog
		else:
			class_ = Event

		new_news = id_ == 'nuevo'

		error = ''

		if not new_news:
			news = class_.get_by_id_(id_)

			if not news:
				error = 'Noticia no encontrado.'

		if not error:
			news_params = {'instance': 'nuevo' if new_news else news,
			               'title': title,
			               'description': description}

			res = class_.validate_params(news_params)

			if res:
				class_.edit_instance(news_params)

				self.flush_mc()

			else:
				error = res

		if error:
			params = {'error': error,
			          'title': title,
			          'description': description,
			          'type': CONTENT_TYPES[type_]}

			self.render('admin-noticias-editar.html', params)

		else:
			self.redirect('/admin/noticias')


class AdminNewsDelete(MainHandler):
	def get(self, type_, id_):
		if type_ == 'blog':
			class_ = Blog
		else:
			class_ = Event

		instance = class_.get_by_id_(id_)

		params = {}

		if id_ != 'nuevo' and instance:
			params['instance'] = instance
			params['type'] = CONTENT_TYPES[type_]

		else:
			params['error'] = 'Noticia no encontrada.'

		self.render('admin-noticias-eliminar.html', params)

	def post(self, type_, id_):
		if type_ == 'blog':
			class_ = Blog
		else:
			class_ = Event

		instance = class_.get_by_id_(id_)

		params = {}

		if id_ != 'nuevo' and instance:
			instance.delete_entity()

		else:
			params['error'] = 'Noticia no encontrada.'

		self.redirect('/admin/noticias')


class Webmap(MainHandler):
	def get(self):
		self.response.out.write('')


class Error404(MainHandler):
	def get(self):
		self.error(404)

		self.render('error-404.html')
