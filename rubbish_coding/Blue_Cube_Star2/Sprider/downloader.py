import hashlib


class Downloader(object):

    def __init__(self, request):

        if str(type(request)) != "<class 'requests.models.Response'>":
            raise ValueError('unavailable request type ')

        self.request = request

    def download(self):
        self.request
        h1 = hashlib.md5()
        h1.update(video_url.encode(encoding='utf-8'))
        name = 'mn' + h1.hexdigest() + '.' + form
        with open(os.path.join('D:\\picture', name), 'wb') as file:
            result = read_time_out(lambda: requests.get(video_url, stream=True, timeout=5))
            read_time_out(lambda: file.write(result.content))
            print(video_url, 'done')


