#!../.venv/bin/python
import argparse, logging, ssl, pathlib
import aiohttp, aiohttp_jinja2, jinja2
from flux.procs import MqttHandler, GrabHandler
from flux.config import load_server_configuration

BASE_DIR =  pathlib.Path().absolute()
PROJECT_ROOT = BASE_DIR / 'flux' / 'web'
PROJECT_SETTINGS = BASE_DIR / 'flux' / 'web'
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Websocket server for monitoring or capture screens")
    parser.add_argument("--cert-file", help="SSL certificate file (for HTTPS)")
    parser.add_argument("--key-file", help="SSL key file (for HTTPS)")
    parser.add_argument("--config", default='config.yaml', help="Config yaml file path", required=False)
    parser.add_argument("--handler", default='capture', help="default handler", required=False)
    args = parser.parse_args()
    server, mqtt, screen = load_server_configuration(args.config)

    ## cert_file in PROJECT_SETTINGS
    #
    if args.cert_file:
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(PROJECT_SETTINGS / args.cert_file, PROJECT_SETTINGS / args.key_file)
    else:
        ssl_context = None

    app = aiohttp.web.Application()
    app['tasks'] = []
    app['sockets'] = {}
    
    ## handler
    #
    if args.handler == 'monitor':
        handler = MqttHandler(app, **mqtt)        
    elif args.handler == 'capture':
        handler = GrabHandler(app, **screen)
    else:
        logger.error('\tHandler unknown. Choose: --handler monitor or --handler capture')
        exit(0)
    logger.info(f'\tUsing handler {args.handler}')
    
    ## routes
    #
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(PROJECT_ROOT / 'templates'))
    app.on_shutdown.append(handler.on_shutdown)
    app.on_startup.append(handler.on_startup)
    app.on_cleanup.append(handler.on_cleanup)
    app.router.add_static('/static/', path=PROJECT_ROOT / 'static', name='static')

    app.add_routes([
        aiohttp.web.get('/', handler.index),
        aiohttp.web.post('/', handler.index),             
        aiohttp.web.get('/ws', handler.ws_manager),
    ])
    aiohttp.web.run_app(app, host=server.get('host'), port=server.get('port'), ssl_context=ssl_context)

