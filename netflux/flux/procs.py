#!.venv/bin/python
import asyncio
import time, json, logging, base64
from threading import Thread, Event
import mss
import cv2
import numpy as np
from flux.tools import MqttBase
from flux.handler import Handler


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Grab():

    def __init__(self, **screen):
        self.full_screen = screen.get('full_screen')
        self.monitor_number = screen.get('monitor_number', 1)
        self.monitor = screen.get('monitor')
        self.display = screen.get('display')
        self.fps = screen.get('fps', 1)  
        
    def millis(self):
        return round(time.time() * 1000)
    
    def frame_delay(self, begin_t):
        duration = float((self.millis() - begin_t)/1000)
        return 1/self.fps - duration
        
    def wait_for_frame(self, begin_t):
        sleep = self.frame_delay(begin_t)
        if sleep > 0:
            Event().wait(sleep)

class Capture(Grab, Thread):

    def __init__(self, producer, **screen):
        Grab.__init__(self, **screen)
        Thread.__init__(self, daemon=True)
        self.producer = producer
        self.stop_event = Event()        
        
    def stop(self):
        self.stop_event.is_set()
        
    def run(self):    
        logger.info(f"\tStart Capture. x11 display {self.display}")
        with mss.mss(display=self.display) as sct:
            monitor = sct.monitors[self.monitor_number]
            if not self.full_screen:
                monitor = self.monitor
            while not self.stop_event.is_set():
                try: 
                    begin_t = self.millis()
                    frame = np.asarray(sct.grab(monitor))
                    success, jpg = cv2.imencode('.jpg', frame)
                    if success:
                        self.producer(jpg.tobytes())
                    self.wait_for_frame(begin_t)
                except Exception as e:
                    logger.error(f"\tCapture error {e}")        
        logger.info(f"\tStop Capture")


class SnoopService(MqttBase):

    def __init__(self, screen, **mqtt):
        super().__init__(**mqtt)
        self.topic = f"{self.topic_base}/screen/{screen.get('title')}"
        self.capture = Capture(self.publish_frame, **screen)
        
    def start_services(self):
        self.capture.start()
        self.startMQTT()

    def stop_services(self):
        self.capture.stop()
        self.stopMQTT()

    def publish_frame(self, frame):
        if frame:
            self._publish_bytes(self.topic, frame)


class MqttService(MqttBase):
    ARGS = dict(org=0, uuid=1, evt=2, title=3)
    
    def __init__(self, **p):
        super().__init__(**p)
        self.register = {}
        self.html = ""
        self.options = []
        
    def args(self, topic, key=None):
        topics = topic.split('/')
        return topics[self.ARGS.get(key)]
    
    def html_select(self):
        html = ['<select id="_uuidopt" onchange="setUUID($(this).val());">'] 
        for opt, lab in self.register.items():
            html.append(f'<option value="{opt}">{lab}</option>') 
        html.append("</select>") 
        return json.dumps('/n'.join(html))

    def _on_bytes_callback(self, topic, payload):       
        buf = base64.b64encode(payload)
        p = f'data:image/jpeg;base64,{buf.decode()}'
        uuid = self.args(topic, 'uuid')
        if not uuid in self.register:
            self.register[uuid] = self.args(topic, 'title')
            self.options.append(uuid)
            self.html = self.html_select()      
        asyncio.run(self.ws_send(**{"topic": topic, "html": self.html, 'options': json.dumps(self.options), "payload": p}))
    async def mqtt_start(self):
        self.client.connect_async(self.host, self.port, self.keepalive)
        self.client.loop_start()


class CaptureService(Grab):

    def __init__(self, **screen):
        super().__init__(**screen)
        self.title = screen.get('title')       
        self.topic = f"{screen.get('topic_base')}/screen/{self.title}"
        
    async def start_capture_service(self):
        logger.info(f"\tStart Capture. x11 display {self.display}")
        with mss.mss(display=self.display) as sct:
            monitor = sct.monitors[self.monitor_number]
            if not self.full_screen:
                monitor = self.monitor

            while True:
                try:                      
                    begin_t = self.millis()
                    frame = np.asarray(sct.grab(monitor))
                    success, jpg = cv2.imencode('.jpg', frame)
                    if success:
                        jpgframe = jpg.tobytes()   
                        buf = base64.b64encode(jpgframe)
                        payload = f'data:image/jpeg;base64,{buf.decode()}'
                        html = json.dumps(f'<span class="w3-text-amber">{self.title}<span>')             
                        await self.ws_send(**{"topic": f'{self.topic}', "html": html, 'options': None, "payload": payload})                        
                    await asyncio.sleep(self.frame_delay(begin_t))
                except Exception as e:
                    logger.error(f"\Capture error {e}")        
        logger.info(f"\tStop Capture")       


class MqttHandler(Handler, MqttService):
    
    def __init__(self, app, **mqtt):
        Handler.__init__(self, app)
        MqttService.__init__(self, **mqtt)
       
    async def on_startup(self, app):
        app['tasks'].append(asyncio.create_task( self.mqtt_start() ))
        
        
class GrabHandler(Handler, CaptureService):
    
    def __init__(self, app, **screen):
        Handler.__init__(self, app) 
        CaptureService.__init__(self, **screen)
        
    async def on_startup(self, app):
        app['tasks'].append(asyncio.create_task( self.start_capture_service() ))

        