#!/usr/bin python3
# -*- coding: utf-8 -*-
import functools
import time
import hashlib
import uuid
import inspect
from config import configs


def decorator_builder(*addition_key):
	def result(method=None, **addition_value):
		if method is None:
			raise KeyError('args method require')

		def decorator(func):
			@functools.wraps(func)
			def wrapper(*args, **kw):
				return func(*args, **kw)
			wrapper.__method__ = method
			for arg_name in addition_key:
				wrapper.__setattr__('__%s__' % arg_name, addition_value[arg_name])
			return wrapper
		return decorator
	return result


def next_id():
	return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


def password(_time):
	s = _time//100000
	sha1 = hashlib.sha1()
	sha2 = hashlib.sha1()
	sha1.update(str(s-1).encode('utf-8') + configs['cloudpiercer']['atomheart']['safety']['salt'].encode('utf-8'))
	sha2.update(str(s).encode('utf-8') + configs['cloudpiercer']['atomheart']['safety']['salt'].encode('utf-8'))
	return [sha1.hexdigest(), sha2.hexdigest()]


def introspection(fn):
	def wrapper(*args, **kwargs):
		return fn(*args, **kwargs)
	args_signature = inspect.signature(fn)
	pk_input = {}
	pk_default = {}
	arg = False
	kw = False
	for name, param in args_signature.parameters.items():
		if param.kind == param.POSITIONAL_OR_KEYWORD:
			if param.default is param.empty:
				pk_input[name] = inspect.Parameter.empty
			else:
				pk_default[name] = param.default
		elif param.kind == param.VAR_POSITIONAL:
			arg = True
		elif param.kind == param.VAR_KEYWORD:
			kw = True
	wrapper.args = arg
	wrapper.kwargs = kw
	wrapper.position_or_keyword_input = pk_input
	wrapper.position_or_keyword_default = pk_default
	wrapper.__name__ == fn.__name__
	return wrapper
	

def str_in_iterable_turns_into_tuple_factory(iterable, address):
	# expect a dict {a:{x:1,y:2,z:3},b:{...},c:{...}}
	def str_in_iterable_turns_into_tuple(iterable):
		# form 'a,b,c,d' to ['a','b','c','d']
		if iterable[address] is None:
			iterable[address] = ''
		if not isinstance(iterable[address], str):
			raise ValueError('only str allowed in this args %s' % iterable[address])
		if iterable[address].rfind(' ') != -1:
			raise ValueError('space not allow in this args %s' % iterable[address])
		str_input = iterable[address]
		a = str_input.rfind(',')
		rs = []
		while a != -1:
			rs_str = str_input[a+1:]
			if rs_str == '' or rs_str == ',':
				raise ValueError('wrong form %s' % iterable[address])
			rs.append(rs_str)
			str_input = str_input[:a]
			a = str_input.rfind(',')
		rs.append(str_input)
		rs.reverse()
		iterable[address] = tuple(rs)
		return iterable
	for keys, values in iterable.items():
		values = str_in_iterable_turns_into_tuple(values)
		iterable[keys] = values

	return iterable


if __name__ == '__main__':
	assa = {'name': {'name': '1,2,3'}}
	rs = str_in_iterable_turns_into_tuple_factory(assa, 'name')
	print(rs)
