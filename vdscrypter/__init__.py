import os
import tempfile
import webbrowser
from pyramid.config import Configurator
from vdscrypter.config import PATH_TO_VDUB, PATH_TO_IM, MEDIA_PLAYER


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
    config.add_route('cleanup', '/cleanup')
    config.scan()
    return config.make_wsgi_app()

missing = {}
if not os.path.exists(os.path.join(PATH_TO_VDUB)):
    missing['VirtualDub'] = os.path.join(PATH_TO_VDUB)
if not os.path.exists(os.path.join(PATH_TO_IM)):
    missing['ImageMagick'] = os.path.join(PATH_TO_IM)
if not os.path.exists(os.path.join(PATH_TO_VDUB)):
    missing['MediaPlayer'] = os.path.join(MEDIA_PLAYER)

if missing:
    for k, v in missing.items():
        print 'Dependency "%s" not found at: "%s" Check config.' % (k, v)
    raise ValueError('Missing %d dependencies.' % len(missing))


TEMP_DIR = tempfile.mkdtemp(prefix="vdscrypter_")

webbrowser.open_new_tab('http://127.0.0.1:6543')

