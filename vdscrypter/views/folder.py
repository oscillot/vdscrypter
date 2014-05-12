import os
import urllib
from pyramid.view import view_config
from pyramid.config import Configurator


SUPPORTED_FILES = ['.gif']
@view_config(route_name='folder', renderer='vdscrypter:templates/folder.mako')
def folder(request):
    folder_path = request.POST.get('folder_path')
    recurse = request.POST.get('recurse', 0)

    found = []
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            for ext in SUPPORTED_FILES:
                if f.endswith(ext):
                    full_path = os.path.join(root, f)
                    relative_path = full_path[len(folder_path):]

                    entry = ('http://127.0.0.1:6543/folder/%s' % relative_path,
                             full_path)

                    if recurse:
                        found.append(entry)
                    else:
                        if root == folder_path:
                            found.append(entry)

    #add a dynamic route to the content, (not thread safe!)
    config = Configurator(registry=request.registry)
    config.add_static_view('folder', folder_path, cache_max_age=3600)
    config.commit()

    return {'found': found,
            'folder_path': folder_path}