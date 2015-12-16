# -*- coding: utf-8 -*-

# Project: "Indavelopers"
# Script: handlers.py - Handlers
# App identifier: indavelopers
# URL: www.indavelopers.com
# Author: Marcos Manuel Ortega - Indavelopers
# Version: v4.0 - 12/2015


# -- Imports --
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
	description = ndb.StringProperty()

	def get_by_id(self):
		pass

	@classmethod
	def get_by_title_url(cls, title_url):
		entity = mc.get('entity-kind={}-title_url={}'.format(cls.__name__, title_url))

		if not entity:
			q_e = cls.query(cls.title_url == title_url, ancestor=model_key(cls.__name__))

			entity = q_e.get()

			mc.set('entity-kind={}-title_url={}'.format(cls.__name__, title_url), title_url)

		return entity

	def validate_params(self):
		pass

	def get_title_url(self):
		pass

	def delete_entity(self):
		pass


class Project(ParentProjectPostEvent):
	type_ = ndb.StringProperty(required=True, choices=['success_cases', 'own_initiative', 'experimentation'])

	@classmethod
	def get_projects(cls):
		projects = mc.get('projects')

		if not projects:
			q_p_sc = cls.query(cls.type_ == 'success_cases', parent=model_key('Project'))
			projects_sc = list(q_p_sc.iter())

			q_p_ow = cls.query(cls.type_ == 'own_initiative', parent=model_key('Project'))
			projects_ow = list(q_p_ow.iter())

			q_p_ex = cls.query(cls.type_ == 'experimentation', parent=model_key('Project'))
			projects_ex = list(q_p_ex.iter())

			projects = {'success_cases': projects_sc,
			            'own_initiative': projects_ow,
			            'experimentation': projects_ex}

			mc.set('projects', projects)

		return projects


class Post(ParentProjectPostEvent):
	@classmethod
	def get_posts(cls, n=0):
		posts = mc.get('posts-n={}'.format(n))

		if not posts:
			q_p = cls.query(parent=model_key('Post')).order(-cls.date)

			if n:
				posts = q_p.fetch(n)
			else:
				posts = q_p.iter()

			posts = list(posts)

			mc.set('posts-n={}'.format(n), posts)

		return posts


class Event(ParentProjectPostEvent):
	@classmethod
	def get_events(cls, n=0):
		events = mc.get('events-n={}'.format(n))

		if not events:
			q_p = cls.query(parent=model_key('Event')).order(-cls.date)

			if n:
				events = q_p.fetch(n)
			else:
				events = q_p.iter()

			events = list(events)

			mc.set('events-n={}'.format(n), events)

		return events
