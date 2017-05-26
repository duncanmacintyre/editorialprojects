# Insert Taskpaper Project from Template
# A workflow for the iOS text editor Editorial
# Copyright (c) 2017 Duncan MacIntyre

# It is recommended to have an understanding of taskpaper before continuing:
# http://omz-software.com/editorial/docs/ios/editorial_writing_todo_lists.html

# This script will allow the user to define taskpaper "templates" for projects, set in 
# /Task Management/Templates.taskpaper in Dropbox. (Their syntax is the same as for regular taskpaper
# projects.) "Variables" can be defined inside of {}

# some terms used in comments:
# - the Templates.taskpaper file is defined as /Task Management/Templates.taskpaper in Dropbox
# - a project is defined as a taskpaper project in Templates.taskpaper
# - a project name is defined as the first line of a taskpaper project, minus the :
# - a project's contents are defined as the whole project, including the first line, tasks, and notes
# - a variable is defined as {variable name} in the Templates.taskpaper file, and the text that will
#   eventually replace this
# - a variable name is defined as the text between { and } for each variable defined in the
#   Templates.taskpaper file

import re
import editor
import dialogs

# the following code:
# 1. gets the contents of the Templates.taskpaper file
# 2. uses a regular expression to find all occurences of a project
# 3. creates a dictionary called templates with items <project name>:<project contents>
templates = {i[1]:i[0] for i in re.findall('((.+):(?:\n.+)+)', editor.get_file_contents('/Task Management/Templates.taskpaper', 'dropbox'))}

# the following code:
# 1. gets the project names (the keys in the templates dictionary)
# 1. uses Editorial's built-in dialogs module to ask the user to choose from a list of these
chosenTemplate = dialogs.list_dialog(title = 'Choose a template:', items = templates.keys())

# if dialog was not cancelled
if chosenTemplate is not None:
	
	# get the project contents corresponding to the chosen project name (the value relating to the chosen key), store this under chosenTemplate
	chosenTemplate = templates[chosenTemplate]
	
	# set up a list to hold variable names
	# (the user will be asked to enter values for these)
	variableNames = []
	# use a regular expression to find each variable in the template contents
	for i in re.finditer('{(.+?)}', chosenTemplate):
		# unless it has already been done, append each variable name to the variableNames list
		if i.group(1) not in variableNames: variableNames.append(i.group(1))
	
	# uses Editorial's built-in dialogs module to ask the user to fill out a form,
	# where there is one text field for each variable found in the variableNames list, store
	# input in variableValues
	# (if no variables are used, an empty dictionary is stored in variableValues instead)
	variableValues = dialogs.form_dialog(title='Enter values for the following variables:', fields=[{'type':'text', 'key':i, 'title':(i.title() + ':')} for i in variableNames]) if len(variableNames) > 0 else {}
	
	# if dialog was not cancelled
	if variableValues is not None:
		# use str.format() to insert the variable values into the template, insert the resulting
		# text into the open document
		editor.insert_text(chosenTemplate.format(**variableValues))
