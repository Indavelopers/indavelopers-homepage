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
import logging

from models import *
from globals import *


# Initialize Jinja2 environment
template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=False)


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

		params = {'page': page or 'inicio'}

		self.render(template, params)


class ProjectsPage(MainHandler):
	def get(self):
		projects = Project.get_projects()

		params = {'projects': projects,
		          'page': 'proyectos'}

		self.render('proyectos.html', params)


class ProjectPage(MainHandler):
	def get(self, title_url):
		project = Project.get_by_title_url(title_url)

		params = {'project': project,
		          'page': 'proyectos'}

		self.render('proyecto.html', params)


class Blog(MainHandler):
	def get(self):
		posts = Post.get_posts()

		params = {'posts': posts,
		          'page': 'blog'}

		self.render('blog.html', params)


class PostPage(MainHandler):
	def get(self, title_url):
		post = Post.get_by_title_url(title_url)

		params = {'post': post,
		          'page': 'blog'}

		self.render('post.html', params)


class Events(MainHandler):
	def get(self):
		events = Event.get_events()

		params = {'events': events,
		          'page': 'eventos'}

		self.render('eventos.html', params)


class EventPage(MainHandler):
	def get(self, title_url):
		event = Event.get_by_title_url(title_url)

		params = {'event': event,
		          'page': 'eventos'}

		self.render('eventos.html', params)


class AutograderPage(MainHandler):
	def get(self, grader_url):
		params = {}

		if grader_url != 'intro-a-gae-wiki':
			params['error'] = ''
		else:
			params['grader_title'] = 'Desarrollo de un portal de wiki'
			params['status'] = False

		self.render('grader.html', params)


class AdminHome(MainHandler):
	def get(self):
		self.render('admin-inicio.html')


class AdminProjects(MainHandler):
	def get(self):
		projects = Project.get_projects()

		params = {'projects': projects}

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
				params['date'] = project.date.strftime('%y/%m/%d %H:%M')
				params['description'] = project.description_md

			else:
				params['error'] = 'Proyecto no encontrado.'

		params['type'] = CONTENT_TYPES[type_]

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

			if res is True:
				project_params['type'] = PROJECTS_TYPES_TRADUCTION[project_params['type']]

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
			params['title'] = project.title
			params['date'] = project.date.strftime('%y/%m/%d %H:%M')
			params['description'] = project.show_description()
			params['type'] = CONTENT_TYPES[type_]

		else:
			params['error'] = 'Proyecto no encontrado.'

		self.render('admin-proyectos-eliminar.html', params)

	def post(self, id_):
		project = Project.get_by_id_(id_)

		error = ''

		if id_ != 'nuevo' and project:
			project.delete_entity()

			self.flush_mc()

		else:
			error = 'Proyecto no encontrado.'

			params = {'error': error}

		if not error:
			self.redirect('/admin/proyectos')

		else:
			self.render('admin-proyectos-eliminar.html', params)


class AdminNews(MainHandler):
	def get(self):
		posts = Post.get_posts()
		events = Event.get_events()

		params = {'posts': posts,
		          'events': events}

		self.render('admin-noticias.html', params)


class AdminNewsEdit(MainHandler):
	def get(self, type_, id_):
		error = ''

		if type_ == 'blog':
			class_ = Post
		elif type_ == 'eventos':
			class_ = Event
		else:
			error = 'Tipo de noticia inv&aacute;lido.'

		new_news = id_ == 'nuevo'

		params = {}

		if not error:
			if not new_news:
				news = class_.get_by_id_(id_)

				if news:
					params['title'] = news.title
					params['date'] = news.date.strftime('%y/%m/%d %H:%M')
					params['description'] = news.description_md
					params['type'] = CONTENT_TYPES[type_]

				else:
					params['error'] = 'Noticia no encontrada.'

		else:
			params['error'] = error

		self.render('admin-noticias-editar.html', params)

	def post(self, type_, id_):
		title = self.request.get('title')
		description = self.request.get('description')

		if type_ == 'blog':
			class_ = Post
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
			               'description': description,
			               'type': type_}

			res = class_.validate_params(news_params)

			if res is True:
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
			class_ = Post
		else:
			class_ = Event

		news = class_.get_by_id_(id_)

		params = {}

		if id_ != 'nuevo' and news:
			params['title'] = news.title
			params['date'] = news.date.strftime('%y/%m/%d %H:%M')
			params['description'] = news.show_description()
			params['type'] = CONTENT_TYPES[type_]

		else:
			params['error'] = 'Noticia no encontrada.'

		self.render('admin-noticias-eliminar.html', params)

	def post(self, type_, id_):
		if type_ == 'blog':
			class_ = Post
		else:
			class_ = Event

		news = class_.get_by_id_(id_)

		error = ''

		if id_ != 'nuevo' and news:
			news.delete_entity()

			self.flush_mc()

		else:
			error = 'Noticia no encontrada.'

			params = {'error': error}

		if not error:
			self.redirect('/admin/noticias')

		else:
			self.render('admin-noticias-eliminar.html', params)


class Webmap(MainHandler):
	def get(self):
		webmap = [URL + u for u in ['/proyectos', '/blog', '/eventos', '/contacto', '/aviso-legal', 'mapa-web']]

		projects = Project.get_projects()
		posts = Post.get_posts()
		events = Event.get_events()

		for k in projects.keys():
			webmap += [URL + '/proyectos/' + i.title_url for i in projects[k]]

		webmap += [URL + '/blog/' + p.title_url for p in posts]
		webmap += [URL + '/eventos/' + e.title_url for e in events]

		webmap = '<br>'.join(webmap)

		self.response.out.write(webmap)


class Error404(MainHandler):
	def get(self):
		self.error(404)

		self.render('error-404.html')
