from Cloudpiercer.some_useful_func import introspection
from Cyberkernal.Exceptions import ExpandRunningException
CYBER = object


def init(cyberkernal):
    global CYBER
    CYBER = cyberkernal


def dictionary_connector(sentence_pattern, attr, results):
    # in this function , we did such: use attr_name to compare with args, then unite to a dictionary post to the
    # function. at last add the fn to the dictionary to the cyberkernal dictionary .
    # patient: using this function, you just have to post args in order
    def decorator(fn):
        def wrapper(*args):
            if len(args) != len(attr):
                raise TypeError('%s expected %s arguments, got %s' % (fn.__name__, len(attr), len(args)))
            return fn(**dict(zip(attr, args)))
        input_set = set(fn.position_or_keyword_input) & set(attr)
        if input_set != fn.position_or_keyword_input:
            raise TypeError('%s expected at least %s arguments, got %s' %
                            (fn.__name__, len(fn.position_or_keyword_input), len(attr)))
        default_set = set(fn.position_or_keyword_default) - input_set
        if default_set & set(attr) != default_set:
            raise ValueError('kw & args not allowed yet. to be continued')
        wrapper.params = attr
        wrapper.results = results
        CYBER.dictionary[sentence_pattern] = wrapper
    return decorator


@introspection
@dictionary_connector('find those * is * in *\'s * ', ('key', 'value', 'database', 'table'), ('data',))
async def fn1(key, value, database, table):
    global CYBER
    r = await CYBER.visit_database('find', database, table, key=key, value=value)
    return r


@introspection
@dictionary_connector('save * in *\'s * ', ('kwargs', 'database', 'table'), (bool,))
async def fn2(kwargs, database, table):
    global CYBER
    r = await CYBER.visit_database('save', database, table, **kwargs)
    return r


@introspection
@dictionary_connector('find the url in *', ('html',), ('url',))
async def fn3(html):
    # when you have to visit an expand, we do so:
    # first, put the function name, a future, and a dictionary of kwargs
    # then the function of the expend will do what they are made for, after which the future will set result
    global CYBER
    future = CYBER.loop.create_future()
    if not getattr(CYBER.running_expand, 'html', None):
        raise ExpandRunningException
    globals()['html_receive_list'].append(CYBER.running_expand['html'],  future, {'html': html})
    result = await future
    return result
