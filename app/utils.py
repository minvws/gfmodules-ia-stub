import configparser

from app.config import YourAppConfig

def load_config(config_file: str) -> YourAppConfig:
    parser = configparser.ConfigParser()
    parser.read(config_file)
    
    config_dict = {section: dict(parser.items(section)) for section in parser.sections()}
    return YourAppConfig(**config_dict)