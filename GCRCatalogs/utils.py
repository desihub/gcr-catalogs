"""
utility module
"""
from astropy.io import fits

__all__ = ['FitsFile']

class FitsFile(object):
    def __init__(self, path):
        self._path = path
        self._file_handle = fits.open(self._path, mode='readonly', memmap=True, lazy_load_hdus=True)
        self.data = self._file_handle[1].data

    def __del__(self):
        del self.data
        del self._file_handle[1].data
        self._file_handle.close()
        del self._file_handle
