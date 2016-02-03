# -*- coding: utf-8 -*-

# Project: "Indavelopers"
# Script: models.py - Datastore models
# App identifier: Indavelopers
# URL: www.indavelopers.com
# Author: Marcos Manuel Ortega - Indavelopers
# Version: v4.0 - 12/2015


# -- Imports --
import urllib
import string
import logging

from globals import *

from google.appengine.ext import ndb
from google.appengine.api import memcache as mc


# -- Parent keys --
def model_key(model, name='default'):
	return ndb.Key(model, name)


# -- Models --
class ParentProjectPostEvent(ndb.Model):
	title = ndb.StringProperty(required=True)
	title_url = ndb.StringProperty(required=True)
	date = ndb.DateTimeProperty(auto_now=True)
	description_html = ndb.StringProperty()
	description_md = ndb.StringProperty()

	@classmethod
	def get_by_id_(cls, id_):
		return cls.get_by_id(int(id_), parent=model_key(cls))

	@classmethod
	def get_by_title_url(cls, title_url):
		title_url = urllib.quote(title_url)

		entity = mc.get('entity-kind={}-title_url={}'.format(cls.__name__, title_url))

		if not entity:
			q_e = cls.query(cls.title_url == title_url, ancestor=model_key(cls.__name__))

			entity = q_e.get()

			mc.set('entity-kind={}-title_url={}'.format(cls.__name__, title_url), entity)

		return entity

	def get_title_url(self):
		return urllib.quote(self.title.replace(u' ', u'-').encode('utf-8'))

	@classmethod
	def _validate_params_base(cls, params):
		error = []

		if not validate_value(params['title'], 'title') or not validate_str(params['title']):
			error.append('T&iacute;tulo inv&aacute;lido.')

		if not validate_str(params['description'], 1400):
			error.append('Descripci&oacute;n inv&aacute;lida.')

		return error

	@classmethod
	def _edit_instance_base(cls, params):
		if params['instance'] == 'nuevo':
			instance = cls(parent=model_key(cls))
		else:
			instance = params['instance']

		instance.title = params['title']
		instance.title_url = instance.get_title_url()
		instance.description_md = params['description']
		instance.description_html = markdown_to_html(instance.description_md)

		return instance

	def delete_entity(self):
		self.key.delete()

	def show_description(self):
		return self.description_html


class Project(ParentProjectPostEvent):
	type_ = ndb.StringProperty(required=True, choices=['success_cases', 'own_initiative', 'experimentation'])

	@classmethod
	def get_projects(cls):
		projects = mc.get('projects')

		if not projects:
			q_p_sc = cls.query(cls.type_ == 'success_cases', ancestor=model_key(cls))
			projects_sc = list(q_p_sc.iter())

			q_p_ow = cls.query(cls.type_ == 'own_initiative', ancestor=model_key(cls))
			projects_ow = list(q_p_ow.iter())

			q_p_ex = cls.query(cls.type_ == 'experimentation', ancestor=model_key(cls))
			projects_ex = list(q_p_ex.iter())

			projects = {'success_cases': projects_sc,
			            'own_initiative': projects_ow,
			            'experimentation': projects_ex}

			mc.set('projects', projects)

		return projects

	@classmethod
	def validate_params(cls, params):
		error = cls._validate_params_base(params)

		if params['type'] != 'casos-exito' and params['type'] != 'iniciativa-propia' \
			and params['type'] != 'experimentacion':
			error += 'Tipo inv&aacute;lido.'

		return '<br>'.join(error) or True

	@classmethod
	def edit_instance(cls, params):
		project = cls._edit_instance_base(params)

		project.type_ = params['type']

		project.put()

		return project


class Post(ParentProjectPostEvent):
	@classmethod
	def get_posts(cls, n=0):
		posts = mc.get('posts-n={}'.format(n))

		if not posts:
			q_p = cls.query(ancestor=model_key('Post')).order(-cls.date)

			if n:
				posts = q_p.fetch(n)
			else:
				posts = q_p.iter()

			posts = list(posts)

			mc.set('posts-n={}'.format(n), posts)

		return posts

	@classmethod
	def validate_params(cls, params):
		error = cls._validate_params_base(params)

		if params['type'] != 'blog':
			error += 'Tipo inv&aacute;lido.'

		return '<br>'.join(error) or True

	@classmethod
	def edit_instance(cls, params):
		post = cls._edit_instance_base(params)

		post.put()

		return post


class Event(ParentProjectPostEvent):
	@classmethod
	def get_events(cls, n=0):
		events = mc.get('events-n={}'.format(n))

		if not events:
			q_p = cls.query(ancestor=model_key(cls)).order(-cls.date)

			if n:
				events = q_p.fetch(n)
			else:
				events = q_p.iter()

			events = list(events)

			mc.set('events-n={}'.format(n), events)

		return events

	@classmethod
	def validate_params(cls, params):
		error = cls._validate_params_base(params)

		if params['type'] != 'eventos':
			error += 'Tipo inv&aacute;lido.'

		return '<br>'.join(error) or True

	@classmethod
	def edit_instance(cls, params):
		event = cls._edit_instance_base(params)

		event.put()

		return event
