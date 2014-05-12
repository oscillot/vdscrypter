import os
import subprocess
from pyramid.view import view_config

from vdscrypter import TEMP_DIR
from vdscrypter.utils.conversions import get_microspf_from_fps

PATH_TO_VDUB = r'c:\users\oscillot\downloads\vdub\vdub64.exe'
PATH_TO_IM = r'C:\Program Files\ImageMagick-6.8.9-Q16\convert'


@view_config(route_name='preview', renderer='json')
def preview(request):
    print TEMP_DIR
    previewer = None
    try:
        # print 'got preview request'
        print request.POST.__dict__

        #get our attributes
        full_path = request.POST.get('full_path')
        orig_name = full_path.rsplit('\\', 1)[1]
        resize = request.POST.get('resize', 'fill')
        bounce = request.POST.get('bounce')
        loop = request.POST.get('loop')
        fps = request.POST.get('fps', '30')
        repeat = request.POST.get('repeat', '1')
        preview = request.POST.get('preview', 'false')

        forward_avi = os.path.join(TEMP_DIR, '%s_forward.avi' % orig_name)
        #render the gif forward and resize/letterbox
        sylia = 'VirtualDub.Open(U"%s");\n' % full_path
        sylia += 'VirtualDub.video.SetFrameRate(%s, 1);\n' % \
            get_microspf_from_fps(fps)
        if resize == 'fill':
                sylia += 'VirtualDub.video.filters.Add("resize");\n'
                sylia += 'VirtualDub.video.filters.instance[0].Config(800, 450, "bilinear", 800, 450, 0);'
        elif resize == 'box':
            sylia += 'VirtualDub.video.filters.Add("resize");\n'
            sylia += 'VirtualDub.video.filters.instance[0].Config(100,100,1,4,3,1,320,240,16,9,3,4,1,0x000000);\n'
            sylia += 'VirtualDub.video.filters.Add("resize");\n'
            sylia += 'VirtualDub.video.filters.instance[1].Config(800,450,0,4,3,0,320,240,4,3,0,4,1,0x000000);\n'
        sylia += 'VirtualDub.SaveAVI(U"%s");' % forward_avi
        tmp_file = os.path.join(TEMP_DIR, "%s_vdtempforward.script" % orig_name)
        with open(tmp_file, 'w') as fp:
            print sylia
            fp.write(sylia)
        subp = subprocess.Popen(r'%s /i %s' % (PATH_TO_VDUB, tmp_file))
        subp.communicate()
        previewer = forward_avi

        #conditionally reverse and render a reverse version
        if bounce == 'true':
            reversed_gif = os.path.join(TEMP_DIR, '%s_reversed.gif' % orig_name)
            reversed_avi = os.path.join(TEMP_DIR, '%s_reversed.avi' % orig_name)
            bounced_avi = os.path.join(TEMP_DIR, '%s_bounced.avi' % orig_name)
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
                sylia += 'VirtualDub.video.filters.instance[0].Config(800, 450, "bilinear", 800, 450, 0);'
            elif resize == 'box':
                sylia += 'VirtualDub.video.filters.Add("resize");\n'
                sylia += 'VirtualDub.video.filters.instance[0].Config(100,100,1,4,3,1,320,240,16,9,3,4,1,0x000000);\n'
                sylia += 'VirtualDub.video.filters.Add("resize");\n'
                sylia += 'VirtualDub.video.filters.instance[1].Config(800,450,0,4,3,0,320,240,4,3,0,4,1,0x000000);\n'
            sylia += 'VirtualDub.SaveAVI(U"%s");' % reversed_avi
            tmp_file = os.path.join(TEMP_DIR, "%s_vdtempreverse.script" % orig_name)
            with open(tmp_file, 'w') as fp:
                print sylia
                fp.write(sylia)
            subp = subprocess.Popen(r'%s /i %s' % (PATH_TO_VDUB, tmp_file))
            subp.communicate()

            sylia = 'VirtualDub.Open(U"%s");\n' % forward_avi
            sylia += 'VirtualDub.Append(U"%s");\n' % reversed_avi
            sylia += 'VirtualDub.SaveAVI(U"%s");\n' % bounced_avi
            tmp_file = os.path.join(TEMP_DIR, "%s_vdtempbounce.script" % orig_name)
            with open(tmp_file, 'w') as fp:
                print sylia
                fp.write(sylia)
            subp = subprocess.Popen(r'%s /i %s' % (PATH_TO_VDUB, tmp_file))
            subp.communicate()

            previewer = bounced_avi

        if loop == 'true' and int(repeat) > 1:
            looped_avi = os.path.join(TEMP_DIR, '%s_looped.avi' % orig_name)
            sylia = 'VirtualDub.Open(U"%s");\n' % previewer
            for r in range(int(repeat) - 1):
                sylia += 'VirtualDub.Append(U"%s");\n' % previewer
            sylia += 'VirtualDub.SaveAVI(U"%s");\n' % looped_avi

            tmp_file = os.path.join(TEMP_DIR, "%s_vdtemplooped.script" % orig_name)
            with open(tmp_file, 'w') as fp:
                print sylia
                fp.write(sylia)
            subp = subprocess.Popen(r'%s /i %s' % (PATH_TO_VDUB, tmp_file))
            subp.communicate()

            previewer = looped_avi

        if preview == 'true':
            # print previewer
            subprocess.Popen('C:\\Program Files (x86)\\Combined Community Codec Pack\\MPC\\mpc-hc.exe %s' % previewer)

    except Exception as e:
        print e
        print e.__class__.__name__
        print e.message

    return {'rendered': previewer}