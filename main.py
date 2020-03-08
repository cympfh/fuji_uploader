import os
import re
from glob import glob
from typing import List

import tornado.ioloop
import tornado.web
from tornado.options import options

ROOT = os.environ.get('FUJI_ROOT', "/media/cympfh/HDCZ-UT/MyPictures/x100f/")
PORT = int(os.environ.get('FUJI_PORT', 8888))


class FileSystem:

    def latest_files(self, num: int) -> List[str]:
        """Enumerate latest file names

        Parameters
        ----------
        num
            number of latest files

        Returns
        -------
        List of file names
            it should be like ["DSCF9000.JPG", ...]
        """
        ret = []
        for d in sorted(glob(f"{ROOT}/*"), reverse=True):
            ret.extend(sorted(glob(f"{d}/*.*"), reverse=True))
            if len(ret) >= num:
                break
        ret = [path.split('/')[-1] for path in ret[:num]]
        return ret

    def exists(self, dirname: str, filename: str) -> bool:
        """Check {ROOT}/{dirname}/{filename} exists"""
        return len(glob(f"{ROOT}/{dirname}/{filename}")) > 0


class FileExistsHandler(tornado.web.RequestHandler):

    def get(self, filepath: str):
        """
        Parameters
        ----------
        filepath
            `DSCF[0-9]{4,4}.*`
        """
        fs = FileSystem()
        latest = fs.latest_files(9999)
        if filepath in latest:
            self.write("Yes")
        else:
            self.write("No")


class UploadHandler(tornado.web.RequestHandler):

    def post(self, filepath: str):
        """
        Parameters
        ----------
        filepath
            `DSCF[0-9]{4,4}.*`
        """
        match = re.match(r'DSCF([0-9]*)\..*', filepath)
        if match is None:
            self.write("Invalid filename")
        else:
            file_num = int(match[1])
            dir_num = 100 + (file_num // 1000)
            fs = FileSystem()
            while fs.exists(f"{dir_num}_FUJI", filepath):
                dir_num += 10
            self.write(f"{dir_num}_FUJI/{filepath}")
            os.makedirs(f"{ROOT}/{dir_num}_FUJI/")
            with open(f"{ROOT}/{dir_num}_FUJI/{filepath}", "wb") as f:
                f.write(self.request.body)


def make_app():
    return tornado.web.Application([
        (r"/exists/(.+)", FileExistsHandler),
        (r"/upload/(.+)", UploadHandler),
    ])


if __name__ == "__main__":
    options.parse_command_line()
    app = make_app()
    app.listen(PORT)
    print(f"Ready -- ROOT = {ROOT}, PORT = {PORT}")
    tornado.ioloop.IOLoop.current().start()
