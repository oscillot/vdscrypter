import os
import subprocess
from pyramid.view import view_config

from vdscrypter import TEMP_DIR

PATH_TO_VDUB = r'c:\users\oscillot\downloads\vdub\vdub64.exe'

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
    subp = subprocess.Popen(r'%s /i %s' % (PATH_TO_VDUB, tmp_file))
    subp.communicate()
    subprocess.Popen('"C:\\Program Files (x86)\\Combined Community Codec Pack\\MPC\\mpc-hc.exe" "%s"' % avi_name)
    return {'output': avi_name}