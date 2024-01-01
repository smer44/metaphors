import os
from ystream.yabstract import yStream


class yFileNamesWalkStream(yStream):

    def __init__(self,rootdir,ext = None, skip_until = None):
        self.init(rootdir,ext,skip_until)

    def init(self,rootdir,ext = None,skip_until = None):
        self.rootdir = rootdir
        assert ext is None or isinstance(ext,str), f"yFileNamesStream.init : set wrong file extention {ext}"
        self.ext = ext
        self.skip_until = skip_until

    def __iter__(self):
        if self.skip_until:
            to_out = False
        else:
            to_out = True
        ext = self.ext
        skip_until = self.skip_until
        for subdir, dirs, files in os.walk(self.rootdir):
            for file in files:
                if ext is None or file.endswith(ext):
                    filepath = subdir + os.sep + file
                    if filepath == skip_until:
                        to_out = True

                    if to_out:
                        yield filepath
                    else:
                        print("yFileNamesStream: skipped", filepath)

