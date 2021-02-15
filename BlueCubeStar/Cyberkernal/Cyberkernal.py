import asyncio
import aiohttp
import config
import functools
from functools import reduce
from Cloudpiercer.some_useful_func import password
import inspect
import time
import os
import threading
from numpy import array
from Cyberkernal.Exceptions import OrderFailedException


class OrderMetaclass(type):
    '''
    the order class should have an attr named
    instruction like this:
    'if you are good, save you in database;if you are bad, save yourself in database.
    calc how good you are now.print it to me.
    for those who good is too low, kill them'
    we will simply translate it into a list like this
    [[[keyword1,keyword2],[keyword3,keyword4]],keyword5,keyword6,(keyword7,)]
    then we will look up the dictionary,translate them like this
    {(0,0,0):fn1,(0,0,1):fn2,.......,(3,):fn5,(4,):fn6}
    meanwhile a variety of args will be inputted as followed

    '''
    def __new__(mcs, name, bases, attrs):
        def explainer(sentence):
            def normal_sentence(n_sentence):
                if n_sentence.find(','):
                    single_order = n_sentence.split(',')
                    return reduce(lambda x1, x2: x1.extend(x2), map(normal_sentence, single_order))
                single_word = n_sentence.split(' ')
                finding_attr = []
                order_sentence = ''
                for item in single_word:
                    if item[0] == '*':
                        finding_attr.append(single_word[0:])
                        order_sentence.join('* ')
                    else:
                        order_sentence.join(item)
                order_sentence.rstrip()
                global CYBER
                if order_sentence not in CYBER.dictionary:
                    raise ValueError('the sentence \'%s\' cannot be translated ' % n_sentence)
                fn = CYBER.dictionary[order_sentence]
                if set(fn.params) != set(finding_attr):
                    raise ValueError('takes argument %s, but %s was given' % (fn.params, finding_attr))
                return fn

            def condition_sentence(c_sentence):
                # double condition is not allowed
                the_rest = c_sentence
                result = []
                the_if = []
                while True:
                    the_next = 'if'
                    m = c_sentence.find('if ')
                    n = c_sentence.find('then ')
                    if n == m == -1:
                        break
                    if m < n & m != -1:
                        if the_next == 'then':
                            raise ValueError('sentence %s error. check if you use double \'if\' ' % c_sentence)
                        s = the_rest[3:n]
                        the_if = normal_sentence(s)
                        the_rest = the_rest[n:]
                        the_next = 'then'
                    if n < m | m == -1:
                        if n == -1:
                            raise ValueError('sentence %s error. check if you use single \'if\' ' % c_sentence)
                        if the_next == 'if':
                            raise ValueError('sentence %s error. check if you use double \'then\' ' % c_sentence)
                        s = the_rest[5:m]
                        the_then = normal_sentence(s)
                        the_rest = the_rest[m:]
                        result += [the_if, the_then]
                return result

            def restriction_sentence(r_sentence):
                # for those who
                result = r_sentence[14:]
                m = result.split(',then ')
                result = map(normal_sentence, m)
                return result

            if sentence.find('if'):
                return condition_sentence(sentence)
            elif sentence.find('for those who'):
                return tuple(['r', restriction_sentence(sentence)])
            else:
                return normal_sentence(sentence)

        if name == 'Order':
            return type.__new__(mcs, name, bases, attrs)
        '''
        won't be edited until I learn NN
        now it will be created by user
        aimed to translate args in Order child class into order_line
        '''
        # here to explain words
        string = attrs['instruction']
        line = {}
        restriction = []
        entropy = 1
        explained_line = []
        args = set()
        results = set()
        instruction_list = string.split('.')
        explained_line += map(explainer, instruction_list)
        for i in explained_line:
            if isinstance(i, tuple):
                if i[0] == 'rs':
                    restriction += i
                    explained_line.remove(i)

        def position_judgement(order_list, position_tuple):
            condition = False
            for j in range(len(order_list)):
                init_list = []
                for k in range(position_tuple):
                    init_list += [0]
                if callable(order_list[j]):
                    line[position_tuple + (i,)] = order_list[j]
                    if condition:
                        line[position_tuple[:-2]].vector.append(init_list[:-2] + list(position_tuple[-2:]))
                        condition = False
                    else:
                        line[position_tuple[:-1] + position_tuple[-1] - 1].vector.append(init_list[:-1] + [1])
                if isinstance(order_list[j], list):
                    condition = True
                    position_judgement(order_list, position_tuple + (j,))

        position_judgement(explained_line, ())
        for i in line.keys():
            if len(i) >= entropy:
                entropy = len(i)
        for i in line.keys():
            rs = i
            while len(i) < entropy:
                rs += (0,)
            line[rs] = line[i]
            line.pop(i)
            while len(line[rs].vector) < entropy:
                line[rs].vector += [0]
            line[rs].vector = array(line[rs].vector)
        for i in line.values():
            args.update(set(i.params))
            results.update(set(i.results))
        input_args = args - args & results
        attrs['line'] = line
        attrs['entropy'] = entropy
        attrs['restriction'] = restriction
        attrs['args'] = args
        attrs['input_args'] = input_args
        attrs['results'] = results
        return type.__new__(mcs, name, bases, attrs)


class Order(dict, metaclass=OrderMetaclass):
    '''
        the metaclass must have done these:
        it has created a list like this
        [(1,2,2,1,3,3)=fn1,(1,3,4,2=fn2)]
        which is used as coordinate
        fn which has some additional args , such as params, vector
        meanwhile some list with be inputted
        entropy(max size of tuple ahead), restriction, args(all the args will be posted),
        input_args(those you must input in advance), results(the result of fn)
        Warning : cannot return to the last status when using OrderMetaclass
    '''

    # self.line ,inherited from list, is simply a list
    # bugs what if three condition lead to one route?
    def __init__(self, **kwargs):
        super().__init__()
        self.update(self.line)
        if set(kwargs.keys()) != self.input_args:
            raise ValueError('takes %s positional argument but %s were given' % (self.input_args, list(kwargs.keys())))
        self.input_args = kwargs
        self.other_option = {}
        self.have_run_position = ()
        self.present_position = (0,)
        self.next_position_vector = ()

    def next_line(self):
        # use vector to judge which way to continue
        if len(self.line[self.present_position].vector) != 1:
            if self.present_position not in self.other_option.keys():
                self.other_option[self.present_position] = self.line[self.present_position].vector
            while list(self.other_option.keys())[-1] is []:
                self.other_option.pop(list(self.other_option.keys())[-1])
                try:
                    self.present_position = list(self.other_option.keys())[-1]
                except IndexError:
                    raise OrderFailedException
            vector = self.other_option[self.present_position][0]
            self.other_option[self.present_position].pop(0)
            v = array(self.present_position) + vector
            self.present_position = tuple(v)
        else:
            self.present_position = tuple(array(self.present_position) + self.line[self.present_position])
        coroutines = self.line[self.present_position]
        return coroutines

    def set_result_to_present_line(self):
        pass

    def set_exception_to_present_line(self):
        pass


class Cyberkernal(object):
    # single object
    # can only be

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.SEM = asyncio.Semaphore(config['cyberkernal']['sem_number'])
        self.client_session = aiohttp.ClientSession()
        self.running_expand = dict()
        self.connected_database = dict()
        self.runnable_expand = dict()
        self.order_list = []
        self._new_expand(*config['cyberkernal']['default_expand'])
        self.dictionary = dict()
        self.scanning()

    def scanning(self):
        while True:
            if self.order_list:
                self.loop.create_task(self.run_order(self.order_list[0]))

    @classmethod
    def _sentinel(cls, ):
        def _function(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kw):
                return fn(*args, **kw)

            return wrapper

        return _function

    def _search_expand_runnable(self):
        route_servers = [x.split('.')[0] for x in os.listdir(os.path.abspath('Expand'))
                         if os.path.splitext(x)[1] == '.py']
        for module_name in route_servers:
            mod = __import__('Expand.' + module_name, globals(), locals(), [module_name])
            self.runnable_expand[mod.__name__] = []
            for attr in dir(mod):
                if attr == 'init':
                    fn = getattr(mod, attr)
                self.runnable_expand[mod.__name__].append(fn)

    @_sentinel()
    def _new_expand(self, expand_name):
        # used to connect an expand known
        expand_list = await self._get('127.0.0.1:8000/cyberkernal/expand_list')
        if (expand_name not in expand_list) | expand_name not in self.runnable_expand:
            raise ValueError('no expand named %s' % expand_name)
        t1 = threading.Thread(target=self.runnable_expand[expand_name])
        self.running_expand[expand_name] = t1

    def _show_expand(self):
        return [key for key in self.running_expand]

    def _kill_expand(self, name):
        # stop an expand, with data saved and quit safely
        self.loop.call_soon(self.running_expand[name].stop())

    def _delete_expand(self):
        # stop a kind of expand on its track
        pass

    async def _get(self, url, bit_num=-1, cookies=None, timeout=None, headers=None):
        # visit an network direction with get method
        def yielder(content):
            if bit_num <= 0:
                return content
            else:
                yield content(bit_num)

        async with self.SEM:
            async with self.client_session as session:
                resp = await session.post(url,
                                          cookies=cookies,
                                          timeout=timeout,
                                          headers=headers)
        return yielder(resp.content)

    async def _post(self, url, cookies=None, timeout=None, headers=None, **kwargs, ):
        # visit an network direction with post method
        async with self.SEM:
            async with self.client_session as session:
                resp = await session.post(url,
                                          data=kwargs,
                                          cookies=cookies,
                                          timeout=timeout,
                                          headers=headers)
        return resp

    async def run_order(self, order):
        task = self.loop.create_task(order.next_line())
        result = await task
        order.set_result_to_present_line(result)

    def communication(self):
        pass

    def communication_file(self):
        pass

    def new_cyber_process(self):
        # create a new process running cyberkernal
        pass

    def cancel_cyber_process(self):
        # just as what is says
        pass

    def kill_cyber_process(self):
        # just as what it says
        pass

    def init_database(self, database_name, database_url=config['database']['url']):
        pw = password(time.time)
        r = await self._get(database_url.join('%s/init/%s' % (database_name, pw)))
        s = {'url': database_url}
        s.update(r)
        self.connected_database[database_name] = s

    def visit_database(self, method, database_name, table, **kwargs):
        # first , it get the database that have been logged in
        # let's take test.write_in and test.write_out for an example
        if database_name not in self.connected_database:
            raise ValueError('%s not init' % database_name)
        info = self.connected_database[database_name]
        if method not in info:
            raise
        fn = info[method]['fn']
        url = info[method]['url']
        args_that_must_be_inputted = info[method]['pk_input']
        args_that_do_not_have_to_be_inputted = info[method]['pk_default']
        # first, for we have run init, we are for sure have info about test, include fn it has, url linked to fn, args
        for kw_name, kw_value in kwargs:
            if kw_name in args_that_do_not_have_to_be_inputted:
                args_that_do_not_have_to_be_inputted[kw_name] = kw_value
            elif kw_name in args_that_must_be_inputted:
                args_that_must_be_inputted[kw_name] = kw_value
            else:
                raise (Warning('unnecessary args received'))
        if inspect.Parameter.empty in args_that_do_not_have_to_be_inputted.values():
            raise TypeError('%s of %s in %s takes %s(must) and %s (optional) positional argument but %s were given'
                            % (fn.__name__, table, database_name, str(list(args_that_must_be_inputted.keys())),
                               str(list(args_that_do_not_have_to_be_inputted.keys())), str(list(kwargs.keys()))))
        # then we do so: make sure kw be argued, arg be argued, args not allowed, every param being inputted
        # the way we do so is by compare kwargs with fn.param
        # warning : *args,**kw not allowed
        r = await self._post(url, **kwargs)
        return r


CYBER = Cyberkernal()
