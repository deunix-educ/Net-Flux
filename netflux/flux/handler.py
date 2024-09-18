import logging, json
import aiohttp, aiohttp_jinja2
import asyncio
from flux import tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Handler():

    def __init__(self, app):
        self.app = app

    def context(self, **ctx):
        return dict(**ctx)
    
    async def websocket_consumer(self, payload):
        await asyncio.sleep(0.25)
       
    async def ws_send(self, **payload):
        for ws in self.app['sockets'].values():
            await ws.send_json(dict(**payload))
            
    async def index(self, request):
        return aiohttp_jinja2.render_template('index.html', request, self.context())

    
    async def ws_manager(self, request):
        ws = aiohttp.web.WebSocketResponse()
        ready = ws.can_prepare(request)
        if not ready.ok:
            return self.index(request)
        await ws.prepare(request)

        key = tools.random_chars()
        request.app['sockets'][key] = ws

        while True:
            msg = await ws.receive()
            #logger.info(f'ws_manager receive: {msg}')
            if msg.type == aiohttp.WSMsgType.text:
                payload = json.loads(msg.data)
                await self.websocket_consumer(payload)

            elif msg.type == aiohttp.WSMsgType.CLOSED:
                logger.info(f'ws_manager CLOSED: {msg.type}')
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                logger.info(f'ws_manager ERROR: {msg.type}')
                break
            else:
                break

        del request.app['sockets'][key]
        logger.info(f'\tKey {key} is being disconnected')
        return ws

    async def on_shutdown(self, app):
        logger.info('\ton_shutdown')
        raise
    
    async def on_startup(self, app):
        logger.info('\ton_startup create tasks in this order')

    async def on_cleanup(self, app):
        logger.info('\ton_cleanup cancel tasks')
        for task in app['tasks']:
            task.cancel()
            await task
            
            