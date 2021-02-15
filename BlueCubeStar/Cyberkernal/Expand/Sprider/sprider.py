import os
import re
import asyncio
import aiohttp
import aiofiles
import hashlib



# you have lost





PATH = 'F:\\3'
PAGE_URL = dict()
# a bug   TASK += list(filter((lambda k:
# asyncio.run_coroutine_threadsafe((RequestType(main_url + k)), loop), second_handled)))
# link with database
HTML_URL = list()
PREY_URL = list()
re_url_html = re.compile(r'/play\.php\?[0-9a-zA-Z\_=%]*')
re_url_page = re.compile(r'/search\.php\?k=!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!&page=\d{1,4]')
re_url_prey = re.compile(r'/xvtest\.php\?id=/video\d*/\d{1,2}\.\d{1,2}\_')
re_url_prey_real = re.compile(r'https://video*')
re_quote = re.compile(r'[\'\"]')


class RequestType(object):

    def __init__(self, url, info_type, byte=40, cookie=None, header=None, ssl=False, sem_number=4):

        self.url = url
        self.info_type = info_type
        self.cookie = cookie
        self.header = header
        self.ssl = ssl
        self.byte = byte
        self.SEM = asyncio.Semaphore(sem_number)
        self.client_session = aiohttp.ClientSession()

    async def __aenter__(self):
        resp = await self.aio_get_response()
        self.resp = resp

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.resp.__aexit__(exc_type, exc_val, exc_tb)
        await self.SEM.__aexit__(exc_type, exc_val, exc_tb)
        await self.client_session.__aexit__(exc_type, exc_val, exc_tb)
        return 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            r = await self.resp.content.read(self.byte)
        except Exception:
            print('timeout')
            r = None
        if not r:
            raise StopAsyncIteration
        return r

    async def aio_get_response(self):
        await self.SEM.__aenter__()
        session = await self.client_session.__aenter__()
        try:
            resp = await session.request('GET',
                                         self.url,
                                         cookies=self.cookie,
                                         timeout=15,
                                         headers=self.header)
        except Exception:
            print('conenction failed when trying to connect %s' % self.url)
            resp = await session.request('GET', 'https://baidu.com')
        if self.info_type == 'html':
            resp.encoding = 'gbk'
        return resp


async def check(main_url, request, re_method, use_main_url = True):
    async with request:
        try:
            r = (await request.resp.read()).decode()
        except Exception:
            print('get access failed')
            r = ''
        first_handled = re.split(re_quote, r)
        second_handled = list(filter(lambda i: re.match(re_method, i), first_handled))
        if use_main_url:
            second_handled = [main_url + i for i in second_handled]
        return second_handled


async def seek_page(main_url, first_page):
    PAGE_URL[first_page] = False
    next_page_url = await check(main_url, RequestType(first_page, 'html'), re_url_page)
    while True:
        i = 0
        for k in next_page_url:
            if k not in PAGE_URL:
                PAGE_URL[k] = False
                i += 1
                next_page_url = await check(main_url, RequestType(main_url + k, 'html'), re_url_page)
        if i == 0:
            print('seek page coro complete')
            break
        elif i != 1:
            print('something may has missed when seek page')


async def seek_html(main_url ):
    while True:
        i = 0
        for k in PAGE_URL:
            if PAGE_URL[k] == False:
                PAGE_URL[k] = True
                global HTML_URL
                HTML_URL += await check(main_url, RequestType(k, 'html'), re_url_html)
                i += 1
        if i == 0:
            print('seek html coro complete ?')
            await asyncio.sleep(4)


async def seek_prey(main_url, prey_type):
    while True:
        i = 0
        for k in HTML_URL:
            finale = await check(main_url, RequestType(k, 'html'), re_url_prey)
            global PREY_URL
            PREY_URL += finale
            if len(finale) != 1:
                print('Warning! prey seeker unreachable')
                break
            finale = await check(main_url, RequestType(finale[0], 'prey'), re_url_prey_real, use_main_url=False)
            if len(finale) != 1:
                print('Warning! prey seeker unreachable')
                break
            try:
                await download(RequestType(finale[0], py_type, byte=16), PATH, prey_type)
            except Exception:
                print('download failed')
                break
            i += 1
        if i == 0:
            print('seek prey coro complete ?')
            await asyncio.sleep(4)


async def download(request, path, prey_type):
    h1 = hashlib.md5()
    print(request.url, 2)
    h1.update(request.url.encode(encoding='utf-8'))
    if prey_type is None:
        path_name = os.path.join(path, h1.hexdigest() + '.' + request.url[request.url.rfind('.') + 1:])
    else:
        path_name = os.path.join(path, h1.hexdigest() + '.' + prey_type)
    async with request:
        async for i in request:
            async with aiofiles.open(path_name, mode='ab') as f:
                await f.write(i)
        print('file %s has downloaded' % path_name)


async def check_task():
    while True:
        global TASK
        TASK = list(filter(lambda i: i.done(), TASK))
        await asyncio.sleep(3)


if __name__ == '__main__':
    Page = seek_page('https, 'https://www.om/search.php?k=%E5%B9%BC')
    Html = seek_html('https://wwbv.com')
    Prey = seek_prey('https://ww.com', 'mp4')
    loop = asyncio.get_event_loop()
    t = asyncio.gather(Page, Html, Prey)
    loop.run_until_complete(t)

