import os
import webbrowser
import subprocess
import tempfile
from pyramid.view import view_config

from vdscrypter.utils.conversions import get_microspf_from_fps

PATH_TO_VDUB = r'c:\users\oscillot\downloads\vdub\vdub64.exe'
PATH_TO_IM = r'C:\Program Files\ImageMagick-6.8.9-Q16\convert'


@view_config(route_name='preview', renderer='json')
def preview(request):
    tmp_dir = tempfile.mkdtemp(prefix="vdscrypter_")
    print tmp_dir
    try:
        # print 'got preview request'
        print request.POST.__dict__

        #get our attributes
        full_path = request.POST.get('full_path')
        fps = request.POST.get('fps')
        resize = request.POST.get('resize', 'fill')
        bounce = request.POST.get('bounce')
        loop = request.POST.get('loop')
        repeat = request.POST.get('repeat', '1')

        forward_avi = os.path.join(tmp_dir, 'forward.avi')
        #render the gif forward and resize/letterbox
        sylia = 'VirtualDub.Open(U"%s");\n' % full_path
        sylia += 'VirtualDub.video.SetFrameRate(%s, 1);\n' % \
            get_microspf_from_fps(fps)
        if resize == 'fill':
            sylia += 'VirtualDub.video.filters.Add("resize");\n'
            sylia += 'VirtualDub.video.filters.instance[0].Config(100,100,1,4,3,1,320,240,16,9,3,4,1,0x000000);\n'
        elif resize == 'box':
            sylia += 'VirtualDub.video.filters.Add("resize");\n'
            sylia += 'VirtualDub.video.filters.instance[0].Config(100,100,1,4,3,1,320,240,16,9,3,4,1,0x000000);\n'
            sylia += 'VirtualDub.video.filters.Add("resize");\n'
            sylia += 'VirtualDub.video.filters.instance[1].Config(800,450,0,4,3,0,320,240,4,3,0,4,1,0x000000);\n'
        sylia += 'VirtualDub.SaveAVI(U"%s");' % forward_avi
        tmp_file = os.path.join(tmp_dir, "vdtempforward.script")
        with open(tmp_file, 'w') as fp:
            print sylia
            fp.write(sylia)
        subp = subprocess.Popen(r'%s /i %s' % (PATH_TO_VDUB, tmp_file))
        subp.communicate()
        previewer = forward_avi

        #conditionally reverse and render a reverse version
        if bounce == 'true':
            reversed_gif = os.path.join(tmp_dir, 'reversed.gif')
            reversed_avi = os.path.join(tmp_dir, 'reversed.avi')
            bounced_avi = os.path.join(tmp_dir, 'bounced.avi')
            subp = subprocess.Popen(
                '%s "%s" -coalesce -reverse -quiet '
                '-layers OptimizePlus  -loop 0 %s' % (PATH_TO_IM,
                                                      full_path,
                                                      reversed_gif))
            subp.communicate()
            sylia = 'VirtualDub.Open(U"%s");\n' % reversed_gif
            sylia += 'VirtualDub.video.SetFrameRate(%s, 1);\n' % \
                get_microspf_from_fps(fps)
            if resize == 'fill':
                sylia += 'VirtualDub.video.filters.Add("resize");\n'
                sylia += 'VirtualDub.video.filters.instance[0].Config(100,100,1,4,3,1,320,240,16,9,3,4,1,0x000000);\n'
            elif resize == 'box':
                sylia += 'VirtualDub.video.filters.Add("resize");\n'
                sylia += 'VirtualDub.video.filters.instance[0].Config(100,100,1,4,3,1,320,240,16,9,3,4,1,0x000000);\n'
                sylia += 'VirtualDub.video.filters.Add("resize");\n'
                sylia += 'VirtualDub.video.filters.instance[1].Config(800,450,0,4,3,0,320,240,4,3,0,4,1,0x000000);\n'
            sylia += 'VirtualDub.SaveAVI(U"%s");' % reversed_avi
            tmp_file = os.path.join(tmp_dir, "vdtempreverse.script")
            with open(tmp_file, 'w') as fp:
                print sylia
                fp.write(sylia)
            subp = subprocess.Popen(r'%s /i %s' % (PATH_TO_VDUB, tmp_file))
            subp.communicate()

            sylia = 'VirtualDub.Open(U"%s");\n' % forward_avi
            sylia += 'VirtualDub.Append(U"%s");\n' % reversed_avi
            sylia += 'VirtualDub.SaveAVI(U"%s");\n' % bounced_avi
            tmp_file = os.path.join(tmp_dir, "vdtempbounce.script")
            with open(tmp_file, 'w') as fp:
                print sylia
                fp.write(sylia)
            subp = subprocess.Popen(r'%s /i %s' % (PATH_TO_VDUB, tmp_file))
            subp.communicate()

            previewer = bounced_avi

        print 4
        if loop == 'true' and int(repeat) > 1:
            looped_avi = os.path.join(tmp_dir, 'looped.avi')
            sylia = 'VirtualDub.Open(U"%s");\n' % previewer
            for r in range(int(repeat) - 1):
                sylia += 'VirtualDub.Append(U"%s");\n' % previewer
            sylia += 'VirtualDub.SaveAVI(U"%s");\n' % looped_avi

            tmp_file = os.path.join(tmp_dir, "vdtemplooped.script")
            with open(tmp_file, 'w') as fp:
                print sylia
                fp.write(sylia)
            subp = subprocess.Popen(r'%s /i %s' % (PATH_TO_VDUB, tmp_file))
            subp.communicate()

            previewer = looped_avi

        os.system("start %s" % previewer)

        print 5
    except Exception as e:
        print e.__class__
        print e.message
    print 6
    return {}
