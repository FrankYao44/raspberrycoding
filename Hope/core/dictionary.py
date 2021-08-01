import inspect
from core.Exceptions import ExpandRunningException
from core.config import configs
import asyncio
import motor.motor_asyncio
CYBER = asyncio.get_event_loop()


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


@dictionary_connector('findall * in * of * by *', ('condition','collection', 'database', 'device'), ('result',))
@introspection
async def db_fn1(condition, collection, database, device):
    name = device + database + collection
    if name in CYBER.connected_args:
        collection = CYBER.connection_args[name]
    else:
        if device not in configs['device']:
            raise Exception
        cilent = motor.motor_asyncio.AsyncIOMotorClient(configs['device'][device]['mongodb_address'])
        database = cilent[database]
        collection = database[collection]
        CYBER.connection_args[name] = collection
    r = collection.find(condition)
    return [document for document in await r.to_list()]


