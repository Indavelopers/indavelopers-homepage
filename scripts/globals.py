# -*- coding: utf-8 -*-

# Project: "Indavelopers"
# Script: globals.py - Auxiliary functions and variables
# App identifier: Indavelopers
# URL: www.indavelopers.com
# Author: Marcos Manuel Ortega - Indavelopers
# Version: v4.0 - 12/2015


# -- Imports --
import re


# -- Variables --
URL = 'http://www.indavelopers.com'

CONTENT_TYPES = {'casos-exito': 'Casos de &eacute;xito',
                 'iniciativa-propia': 'Iniciativa propia',
                 'experimentacion': 'Experimentaci&oacute;n',
                 'blog': 'Posts',
                 'eventos': 'Eventos'}

PROJECTS_TYPES_TRADUCTION = {'casos-exito': 'success_cases',
                             'iniciativa-propia': 'own_initiative',
                             'experimentacion': 'experimentation'}


# -- Functions --
def validate_value(value, value_type):
	if type(value) is bool or value is None:
		return value

	elif type(value) is str:
		value = unicode(value, 'utf-8')

	else:
		value = unicode(value)

	if value_type == 'title' and value == 'nuevo':
		return False

	regex_dict = {'id_instance': ur'^\d{1,16}$',
	              'title': ur'^.{6,140}$'}

	regex = re.compile(regex_dict[value_type], re.UNICODE)

	return True if regex.match(value) else False


def validate_str(s, length=140):
	return len(s) <= length if len(s) > 0 else False


def truncate_text(s, length=300):
	return s[:length]


def markdown_to_html(text):
	# todo markdown_to_html()
	return text


def html_to_markdown(text):
	# todo html_to_markdown()
	return text
