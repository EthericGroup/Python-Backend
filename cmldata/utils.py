import os
import configparser


BASE_DIR = os.path.abspath(os.getcwd())

def settings():
    pd = os.path.join(BASE_DIR, os.pardir)
    config_file = os.path.join(pd, 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_file)

    config_dict = {
        'firebase': os.path.join(pd,
                            config['firebase']['CERT_PATH']),
        'github': {
            'secret': config['github']['GIT_SECRET'],
            'id': config['github']['GIT_ID']
        }
    }
    return config_dict