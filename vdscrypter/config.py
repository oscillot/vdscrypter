import os
import json

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'config.json')) as fp:
    config_data = fp.read()

config = json.loads(config_data)

PATH_TO_VDUB = os.path.join(config['virtualdub_directory'], 'vdub64.exe')
PATH_TO_IM = os.path.join(config['imagemagick_directory'], 'convert.exe')
MEDIA_PLAYER = config['media_player_executable']