import os
import codecs
import tempfile

import jinja2
import jinja2.ext

import mf2py

import filters

def _ensure_dir(f):
	d = os.path.dirname(f)
	if not os.path.isdir(d):
		os.makedirs(d)

def _render(note, charset='utf-8'):

	# load from FileSystem directory
	loader = jinja2.FileSystemLoader('templates')

	# create environment and set to strip code blocks
	env = jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True, extensions=[jinja2.ext.with_])

	# add datetime formatting filter
	env.filters['dtformat'] = filters.dtformat

	# render template and return
	return env.get_template('manifold-note.html').render(note=note)

def create(storage, data):

	# get uid and use as file name
	try:
		uid = data['properties']['uid'][0]
		uid = uid.strip()

		if not uid:
			return {'code': 400, 'message': 'uid of data not valid'}
	except KeyError:
		return {'code': 400, 'message': 'uid of data not found'}
		pass

	path = os.path.join(storage, 'notes', uid, uid+'.html')

	# make sure the directories exist
	_ensure_dir(path)

	#  if file already exists return error
	if os.path.exists(path):
		return {'code': 409, 'message': 'File already exists'}

	# create a file;
	with codecs.open(path, 'w', 'utf-8') as f:
		f.write(_render(data['properties']))

	return {'code': 200, 'message': 'File stored'}

def read(storage, uid):

	path = os.path.join(storage, 'notes', uid, uid+'.html')

	if os.path.exists(path):

		with codecs.open(path, 'r', 'utf-8') as f:
			data = mf2py.Parser(doc=f).to_dict(filter_by_type='h-entry')
		# only return the first h-entry
		return {'code': 200, 'message': 'File read', 'data': data[0]}

	else:
		return {'code': 404, 'message': 'File not found'}

def update(storage, data):

	# get uid and use as file name
	try:
		uid = data['properties']['uid'][0]
		uid = uid.strip()

		if not uid:
			return {'code': 400, 'message': 'uid of data not valid'}
	except KeyError:
		return {'code': 400, 'message': 'uid of data not found'}
		pass

	# open file. if does not exist throw error
	dir_path = os.path.join(storage, 'notes', uid)
	path = os.path.join(dir_path, uid+'.html')

	if os.path.exists(path):
		old_data = None

		with codecs.open(path, 'r', 'utf-8') as f:
			old_data = mf2py.Parser(doc=f).to_dict(filter_by_type='h-entry')

		# don't allow uid change through update
		if old_data['properties']['uid'][0] == uid:

			# create temp file to write data
			with tempfile.NamedTemporaryFile(delete=False, dir=dir_path) as temp_f:
				temp_f.write(_render(data['properties']).encode('utf-8'))
				# replace original file
				os.rename(temp_f.name, path)

			return {'code': 200, 'message': 'File updated'}

		else:
			return {'code': 400, 'message': 'uid of data does not match uid of file'}

	else:
		return {'code': 404, 'message': 'File not found'}

	# return status of update
	return None

def extend(storage, uid, data):

	# used to add some properties to the file such as syndication links, responses without changing the whole file

	# return status of extend
	return None

def delete(storage, uid):

	# find file. raise error if does not exist

	# delete file? or just flag?

	# return status of delete
	return None
