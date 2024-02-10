import configparser # for reading the config file
import logging      # for logging errors
import traceback    # for printing exceptions
import sys          # for logging to stdout

def interpret_log_level(log_level):
    """ Given a log level string, returns the corresponding log level integer from the logging library """
    return {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
        }.get(log_level.upper(), logging.WARNING) # default to WARNING if the log level is not recognized


def get_config():
    """ Import the config file and return the data object """
    try:
        raw_config = configparser.ConfigParser()
        raw_config.read('config.ini')
    except FileNotFoundError:
        print("Error reading config file")
        traceback.print_exc()
        exit(1)
    
    try:
        class config:
            def __init__(self):
                config_log_level = raw_config.get('APPLICATION', 'logLevel', fallback='WARNING')
                self.log_level = interpret_log_level(config_log_level)

                self.api_key = raw_config['OPENWEATHER']['apiKey']

                self.units = raw_config['OPENWEATHER']['units']
                self.render_method = raw_config['APPLICATION']['renderMethod']

                self.city_one_name = raw_config['OPENWEATHER']['city1Name']
                self.city_one_lat = raw_config['OPENWEATHER']['city1Lati']
                self.city_one_lon = raw_config['OPENWEATHER']['city1Long']

                if raw_config['OPENWEATHER']['city2Lati'] != 'latitude':
                    self.mode = 'dual'
                    self.city_two_name = raw_config['OPENWEATHER']['city2Name']
                    self.city_two_lat = raw_config['OPENWEATHER']['city2Lati']
                    self.city_two_lon = raw_config['OPENWEATHER']['city2Long']
                else:
                    self.mode = 'single'
    except Exception:
        print("Error parsing config file")
        traceback.print_exc()
        exit(1)
        
    output = config()
    return output


def start_logging(log_level):
    """Set up logging for the main application, with a log object that can be passed to methods"""
    class track:
        """ A class to hold the logger and handlers for application runtime data tracking """
        def __init__(self):
            self.logger = logging.getLogger()
            self.logger.setLevel(log_level)

            self.file_handler = logging.FileHandler('weatherDisplay.log')
            self.file_handler.setLevel(log_level)

            self.stdout_handler = logging.StreamHandler(sys.stdout)
            self.stdout_handler.setLevel(log_level)

            self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')

            self.file_handler.setFormatter(self.formatter)
            self.stdout_handler.setFormatter(self.formatter)

            self.logger.addHandler(self.file_handler)
            self.logger.addHandler(self.stdout_handler)
    output = track()
    return output
