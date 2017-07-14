import threading

def make_template_name( user, template_name ):
    return "{}.{}".format(user,template_name)


class SafeDict(dict):
    def __init__(self, *args):
        self._lockobj = threading.Lock()
        dict.__init__(self, args)

    def __getitem__(self, key):
        try:
            self._lockobj.acquire()
            val = dict.__getitem__(self, key)
        except:
            raise
        finally:
            self._lockobj.release()

    def __setitem__(self, key, value):
        try:
            self._lockobj.acquire()
            dict.__setitem__(self, key, value)
        except:
            raise
        finally:
            self._lockobj.release()

