import os
import shutil
import tempfile
import webbrowser
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('folder', '/folder')
    config.add_route('preview', '/preview')
    config.add_route('render', '/render')
    config.scan()
    return config.make_wsgi_app()

TEMP_DIR = tempfile.mkdtemp(prefix="vdscrypter_")

#clean up old
for root, dirs, files in os.walk('C:\\Users\\Oscillot\\AppData\\Local\\Temp'):
    for d in dirs:
        if d.startswith('vdscrypter'):
            shutil.rmtree(os.path.join(root, d))

webbrowser.open_new_tab('http://127.0.0.1:6543')

