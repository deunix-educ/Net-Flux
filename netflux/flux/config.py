#
from flux import tools

def load_server_configuration(conf_file):
    settings = tools.yaml_load(conf_file)
    server = settings['server']
    mqtt = settings['mqtt']
    screen = settings['screen']
    
    if not server['uuid']:
        uuid = f'0x{tools.gen_device_uuid()}'
        org = mqtt['org']
        server['uuid'] = uuid
        server['topic_base'] = f"{org}/{uuid}"
        server['topic_subs']= [ [f"{org}/+/screen/#", 0], ]      
        tools.yaml_save(conf_file, settings)
        
    mqtt.update({
        'uuid': server.get('uuid'), 
        'topic_base': server.get('topic_base'), 
        'topic_subs': server.get('topic_subs')
    })
    return server, mqtt, screen


def load_screen_configuration(conf_file):
    settings = tools.yaml_load(conf_file)
    mqtt = settings['mqtt']
    screen = settings['screen']
    
    if not settings['screen']['uuid']:
        uuid = f'0x{tools.gen_device_uuid()}'
        org = mqtt['org']
        screen['uuid'] = uuid
        screen['topic_base'] = f"{org}/{uuid}"
        screen['topic_subs']= [ [f"{org}/{uuid}/screen/#", 0], ]     
        tools.yaml_save(conf_file, settings)
        
    mqtt.update({
        'uuid': screen.get('uuid'), 
        'topic_base': screen.get('topic_base'), 
        'topic_subs': screen.get('topic_subs')
    })
    return screen, mqtt
