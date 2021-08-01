from some_useful_func import introspection
from Cyberkernal.Exceptions import ExpandRunningException
import asyncio
CYBER = object


def dict_init(cyberkernal):
    global CYBER
    CYBER = cyberkernal

    def dictionary_connector(sentence_pattern, attr, results):
        # in this function , we did such: use attr_name to compare with args, then unite to a dictionary post to the
        # function. at last add the fn to the dictionary to the cyberkernal dictionary .
        # patient: using this function, you just have to post args in order
        # usually results ordered by time
        def decorator(fn):
            def wrapper(**kwargs):
                if tuple(kwargs.keys()) != attr:
                    raise TypeError('%s expected %s arguments, got %s' % (fn.__name__, list(kwargs.keys()), attr))
                return fn(**dict(**kwargs))

            input_set = set(fn.position_or_keyword_input) & set(attr)
            if input_set != set(fn.position_or_keyword_input.keys()):
                raise TypeError('%s expected at least %s arguments, got %s' %
                                (fn.__name__, fn.position_or_keyword_input, attr))
            default_set = set(fn.position_or_keyword_default) - input_set
            if default_set & set(attr) != default_set:
                raise ValueError('kw & args not allowed yet. to be continued')
            wrapper.params = attr
            wrapper.results = results
            CYBER.dictionary[sentence_pattern] = wrapper

        return decorator


    @dictionary_connector('find those * is * in * \'s * ', ('key', 'value', 'database', 'table'), ('data',))
    @introspection
    async def fn1(key, value, database, table):
        global CYBER
        r = await CYBER.visit_database('find', database, table, key=key, value=value)
        return r


    @dictionary_connector('save * in * \'s * ', ('kwargs', 'database', 'table'), (bool,))
    @introspection
    async def fn2(kwargs, database, table):
        global CYBER
        r = await CYBER.visit_database('save', database, table, **kwargs)
        return r

    @dictionary_connector('show * ', ('data',), ())
    @introspection
    async def fn3(data):
        print(data)
        await asyncio.sleep(1)
        print(data)

    @dictionary_connector('test *', ('number',), ('calc_result',))
    @introspection
    async def test_fn1(number):
        global CYBER
        future = CYBER.loop.create_future()
        if not getattr(CYBER.running_expand, 'test', None):
            raise ExpandRunningException
        globals()['test_receive_list'].append([CYBER.running_expand['test'], future, {'number': number}])
        result = await future
        return result


    @dictionary_connector('find the url in *', ('html',), ('url',))
    @introspection
    async def html_fn1(html):
        # when you have to visit an expand, we do so:
        # first, put the function name, a future, and a dictionary of kwargs
        # then the function of the expend will do what they are made for, after which the future will set result
        global CYBER
        future = CYBER.loop.create_future()
        if not getattr(CYBER.running_expand, 'html', None):
            raise ExpandRunningException
        globals()['html_receive_list'].append([CYBER.running_expand['html'], future, {'html': html}])
        result = await future
        return result



