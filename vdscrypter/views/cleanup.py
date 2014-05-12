import os
import shutil
from pyramid.view import view_config


@view_config(route_name='cleanup', renderer='json')
def cleanup(request):
    #clean up old
    for root, dirs, files in os.walk('C:\\Users\\Oscillot\\AppData\\Local\\Temp'):
        for d in dirs:
            if d.startswith('vdscrypter'):
                shutil.rmtree(os.path.join(root, d))
    print 'This house is clean!'
    return {}
