#!../.venv/bin/python
import argparse, logging
from flux.procs import SnoopService
from flux.config import load_screen_configuration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    

def main(conf_file):
    snoop = None
    try:
        screen, mqtt = load_screen_configuration(conf_file)
        snoop = SnoopService(screen, **mqtt)
        snoop.start_services()      
    except Exception as e:
        logger.info(f'End of SnoopService process: {e}')
    finally:
        if snoop:
            snoop.stop_services()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Screen capture service")
    parser.add_argument("--config", default='config.yaml', help="Config yaml file path", required=False)
    args = parser.parse_args()
    if args.config:
        main(args.config)
        
