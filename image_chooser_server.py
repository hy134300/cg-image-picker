from server import PromptServer
from aiohttp import web
import time

class Cancelled(Exception):
    pass

class MessageHolder:
    messages = {}
    lastCancel = time.monotonic()

    @classmethod
    def _addCancel(cls):
        cls.lastCancel = time.monotonic()

    @classmethod
    def _recentCancel(cls, period=1.0):
        return ((time.monotonic()-cls.lastCancel)<period)
    
    @classmethod
    def addMessage(cls, id, message):
        if message=='__cancel__':
            cls._addCancel()
        elif message=='__start__':
            cls.messages = {}
        else:
            cls.messages[str(id)] = message
    
    @classmethod
    def waitForMessage(cls, id, period = 0.1, asList = False):
        sid = str(id)
        while not (sid in cls.messages) and not ("-1" in cls.messages):
            if cls._recentCancel():
                raise Cancelled()
            time.sleep(period)
        if cls._recentCancel():
            raise Cancelled()
        message = cls.messages.pop(str(id),None) or cls.messages.pop("-1")
        try:
            if asList:
                return [int(x.strip()) for x in message.split(",")]
            else:
                return int(message.strip())
        except ValueError:
            print(f"ERROR IN IMAGE_CHOOSER - failed to parse '${message}' as ${'comma separated list of ints' if asList else 'int'}")
            return [1] if asList else 1

routes = PromptServer.instance.routes
@routes.post('/image_chooser_message')
async def make_image_selection(request):
    post = await request.post()
    MessageHolder.addMessage(post.get("id"), post.get("message"))
    return web.json_response({})