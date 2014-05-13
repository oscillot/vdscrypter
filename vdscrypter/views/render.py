import os
import subprocess
from pyramid.view import view_config

from vdscrypter import TEMP_DIR
from vdscrypter.config import PATH_TO_VDUB, MEDIA_PLAYER

@view_config(route_name='render', renderer='json')
def render(request):
    list_to_render = request.POST.getall('rendered[]')
    compress = request.POST.get('compress', 'true')
    folder_path = request.POST.get('output', '')
    if folder_path == '' or not os.path.exists(folder_path):
        folder_path = request.POST.get('folder_path', '')
    if folder_path.endswith(os.path.sep):
        folder_path = folder_path[:-1]
    avi_name = folder_path + '.avi'
    first = list_to_render[0]
    rest = list_to_render[1:]
    sylia = 'VirtualDub.Open(U"%s");\n' % first
    for each in rest:
        sylia += 'VirtualDub.Append(U"%s");\n' % each
    if compress == 'true':
        sylia += 'VirtualDub.video.SetMode(1);\n'
        sylia += 'VirtualDub.video.SetCompression(0x64697678,0,10000,0);\n'
    sylia += 'VirtualDub.SaveAVI(U"%s");\n' % avi_name
    tmp_file = os.path.join(TEMP_DIR, "output_vdtemprender.script")
    with open(tmp_file, 'w') as fp:
        print sylia
        fp.write(sylia)
    subp = subprocess.Popen(r'%s /i %s' % (os.path.join(PATH_TO_VDUB,
                                                        'vdub64.exe'),
                                           tmp_file))
    subp.communicate()
    subprocess.Popen('"%s" "%s"' % (MEDIA_PLAYER, avi_name))
    return {'output': avi_name}