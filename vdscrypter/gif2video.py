# import os
# import json
# import shutil
# import optparse
# import tempfile
# import traceback
# import subprocess
#
# HERE = os.path.dirname(__file__)
# with open(os.path.join(HERE, 'config.json')) as fp:
#     CONFIG = json.loads(fp.read())
# PATH_TO_VDUB = CONFIG['vdub_path']
# FCC_HANDLERS = CONFIG['fourcc_handlers']
#
# parser = optparse.OptionParser()
# parser.add_option("-f", "--file", dest="file", help="the input file", metavar="FILE")
# parser.add_option("-d", "--dir", dest="file_dir", help="a directory with at least one supported file")
# parser.add_option("-l", "--loops", dest="loops", help="number of times to loop each file")
# parser.add_option("-t", "--types", dest="itypes", help="the types of inputs to accept")
# parser.add_option("-a", "--avi", dest="avi", help="the output avi file or folder (optional)", metavar="FILE")
# parser.add_option("-r", "--resize", dest="resize", help="Default is _off_ for a single file and on for multiple.")
# parser.add_option("-x", "--x", dest="x", help="desired width of video if resizing (defaults to 800)")
# parser.add_option("-y", "--y", dest="y", help="desired height of video if resizing (defaults to 450)")
# parser.add_option("-s", "--speed", dest="fps", help="number of frames to display per second")
# parser.add_option("-4", "--fourcc", dest="fourcc", help="the fourcc handler to use for compression, if omitted, video is uncompressed, as of now only xvid is supported")
#
# USAGE = "python gif2video.py -f/--file some.file -l/--loops 6 -t/--types gif (-a/--avi some.avi -r/--resize true -x 800 -y 450 -s/--speed 25 -4/--fourcc xvid)\n" \
#         "python gif2video.py -d/--dir /some/dir -l/--loops 6 -t/--types gif (-a/--avi some.avi -r/--resize true -x 800 -y 450 -s/--speed 25 -4/--fourcc xvid)\n" \
#         "python gif2video.py -d \"c:\users\oscillot\Downloads\gifs\gifs\" -l 6 -t gif -s 25 -a c:\users\oscillot\Dropbox\gifvids\test3-xvid.avi -r true -x 800 -y 450 -4 xvid\n" \
#         "python gif2video.py -h/--help"
# tmp_dir = tempfile.mkdtemp()
# temp_avi_dir = os.path.join(tmp_dir, 'avis')
# os.makedirs(temp_avi_dir)
#
#
# def wrapper(options):
#     if (not options.file and not options.file_dir) or not options.loops or not options.itypes: #wrong args
#         print USAGE
#         exit(1)
#     if options.itypes not in CONFIG['input_types'].keys():
#         print 'Input type must be one of: `%s`' % '` `'.join(CONFIG['input_types'].keys())
#     input_ftypes = CONFIG['input_types'][options.itypes]
#     if not options.avi or '.' not in options.avi: #if we have a folder
#         if not options.file:
#             path = options.file_dir
#         else:
#             path, gif_fname = os.path.split(options.file)
#         default_fname = 'gif2video.avi'
#         options.avi = os.path.join(path, default_fname)
#     if options.file and options.file_dir:
#         print "--gif (-g) and --dir (-d) are mutually exclusive."
#         exit(2)
#     if not options.fps:
#         options.fps = '25'
#     gif_list = []
#     if options.file:
#         if not os.path.exists(options.file):
#             print 'Input gif not found, check your path: %s' % options.file
#             exit(3)
#         print options.file
#         gif_list.append(options.file)
#     elif options.file_dir:
#         if not os.path.exists(options.file_dir):
#             print 'Input path not found, check your path: %s' % options.file_dir
#             exit(4)
#         for root, dirs, files in os.walk(options.file_dir):
#             for f in files:
#                 if f[-4:] in input_ftypes or f[-5:] in input_ftypes:
#                     print os.path.join(root, f)
#                     gif_list.append(os.path.join(root, f))
#     if len(gif_list) == 0:
#         print 'No gifs were found!'
#         exit(5)
#     #Default crop to true for multiple images
#     if len(gif_list) < 2 and not options.resize:
#         options.resize = "True"
#     script = ''
#
#     def get_microspf_from_fps(fps):
#         spf = 1/float(fps)
#         mspf = spf * 1000
#         microspf = mspf * 1000
#         return microspf
#
#     for gif in sorted(gif_list):
#         script += 'VirtualDub.Open(U"%s");\n' % gif
#         script += 'VirtualDub.video.SetFrameRate(%s, 1);\n' % get_microspf_from_fps(options.fps)
#         if options.resize and options.resize.lower() in ['on', 'true', '1']:
#             script += 'VirtualDub.video.filters.Add("resize");\n'
#             script += 'VirtualDub.video.filters.instance[0].Config(%(x)s, %(y)s, "bilinear", %(x)s, %(y)s, 0);' % {'x': options.x, 'y': options.y}
#         gifname = os.path.split(gif)[1]
#         script += 'VirtualDub.SaveAVI(U"%s.avi");\n' % os.path.join(temp_avi_dir, gifname)
#
#     avi_list = []
#     for gif in gif_list:
#         avi_list.append(os.path.join(temp_avi_dir, '%s.avi' % os.path.split(gif)[1]))
#     avi_list = sorted(avi_list)
#
#     for i, avi in enumerate(avi_list):
#         for r in range(int(options.loops)):
#             if i == 0:
#                 script += 'VirtualDub.Open(U"%s");\n' % avi
#             else:
#                 script += 'VirtualDub.Append(U"%s");\n' % avi
#
#     if options.fourcc:
#         script += 'VirtualDub.video.SetMode(1);\n'
#         script += 'VirtualDub.video.SetCompression(%s,0,10000,0);\n' % str(FCC_HANDLERS[options.fourcc])
#
#     script += 'VirtualDub.SaveAVI(U"%s");\n' % options.avi
#
#
#     tmp_file = os.path.join(tmp_dir, "vdtemp.script")
#     with open(tmp_file, 'w') as fp:
#         print script
#         fp.write(script)
#     subp = subprocess.Popen(r'%s /i %s' % (PATH_TO_VDUB, tmp_file))
#     subp.communicate()
#
#
# if __name__ == "__main__":
#     options, args = parser.parse_args()
#     try:
#         wrapper(options)
#     except Exception, e:
#         traceback.print_exc()
#     finally:
#         if args:
#             print "\n\tYou also typed: `%s` but we didn't do anything with it. Just thought you should know." % ' '.join(args)
#         shutil.rmtree(tmp_dir)