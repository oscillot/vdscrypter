import os
import shutil
import subprocess
import tempfile
from PIL import Image, ImageOps, ImageSequence
from pyramid.view import view_config

from vdscrypter.utils.conversions import get_microspf_from_fps
from vdscrypter.utils.images2gif import writeGif as write_gif


PATH_TO_VDUB = 'c:\users\oscillot\download\vdub\vdub64.exe'


@view_config(route_name='preview', renderer='json')
def preview(request):
    print 'got preview request'
    print request.POST.__dict__
    full_path = request.POST.get('full_path')
    fps = request.POST.get('fps')
    resize = request.POST.get('resize')
    bounce = request.POST.get('bounce')
    loop = request.POST.get('loop')
    repeat = request.POST.get('repeat')

    tmp_dir = tempfile.mkdtemp()
    gif_name = os.path.join(tmp_dir, 'preview.gif')

    im = Image.open(full_path, 'r')
    if resize == 'fill':
        im.resize((800, 450))
    elif resize == 'box':
        w, h = im.size
        if w <= h:
            border = 800 - w
        else:
            border = 450 - h
        ImageOps.expand(image=im, border=border, fill=0)
        ImageOps.fit(image=im, size=(800, 480), method=Image.ANTIALIAS,
                     bleed=0.0, centering=(0.5, 0.5))
        im.save(gif_name)

    if bounce:
        bounced_name = os.path.join(tmp_dir, 'bounced.gif')
        im = Image.open(gif_name, 'r')
        original_duration = im.info['duration']
        frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
        im.close()
        reversed_frames = reversed(frames)
        write_gif(bounced_name,
                  frames.extend(reversed_frames),
                  duration=original_duration/1000.0, dither=0)
        new_gif = bounced_name
    else:
        new_gif = gif_name


    sylia = 'VirtualDub.Open(U"%s");\n' % new_gif
    sylia += 'VirtualDub.video.SetFrameRate(%s, 1);\n' % \
             get_microspf_from_fps(fps)

    if loop:
        for r in range(repeat - 1):
            sylia += 'VirtualDub.Append(U"%s");\n' % new_gif

    sylia += 'VirtualDub.Preview();'

    tmp_file = os.path.join(tmp_dir, "vdtemp.script")
    with open(tmp_file, 'w') as fp:
        print sylia
        fp.write(sylia)
    subp = subprocess.Popen(r'%s /i %s' % (PATH_TO_VDUB, tmp_file))
    subp.communicate()

    shutil.rmtree(tmp_dir)
    return {}
