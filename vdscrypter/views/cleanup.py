import os
import shutil
from pyramid.view import view_config


@view_config(route_name='cleanup', renderer='json')
def cleanup(request):
    #clean up old
    for root, dirs, files in os.walk('C:\\Users\\Oscillot\\AppData\\Local\\Temp'):
        for f in files:
            if 'vdscrypter_' in root:
                os.remove(os.path.join(root, f))
    for root, dirs, files in os.walk('C:\\Users\\Oscillot\\AppData\\Local\\Temp'):
        for d in dirs:
            if d.startswith('vdscrypter_'):
                try:
                    os.removedirs(os.path.join(root, d))
                except WindowsError as e:
                    print e
    print 'This house is clean!'
    return {}
