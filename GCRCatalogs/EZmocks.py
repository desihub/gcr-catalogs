"""
EZMock galaxy catalog class.
"""
from __future__ import division, print_function
import os
import re
import functools
import numpy as np
from astropy.io import fits
from astropy.cosmology import FlatLambdaCDM
from GCR import BaseGenericCatalog

__all__ = ['EZMockGalaxyCatalog']


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


class EZMockGalaxyCatalog(BaseGenericCatalog):
    """
    EZmocks galaxy catalog class. Uses generic quantity and filter mechanisms
    defined by BaseGenericCatalog class.
    """

    def _subclass_init(self,
                       catalog_root_dir,
                       catalog_path_template,
                       cosmology,
                       halo_mass_def=None,
                       lightcone=True,
                       sky_area=14000.0,
                       use_cache=True,
                       **kwargs):

        assert(os.path.isdir(catalog_root_dir)), 'Catalog directory {} does not exist'.format(catalog_root_dir)

        self._catalog_path_template = {k: os.path.join(catalog_root_dir, v) for k, v in catalog_path_template.items()}
        self._default_subset = 'truth' if 'truth' in self._catalog_path_template else next(iter(self._catalog_path_template.keys()))

        self._native_filter_quantities = {}

        self.cache = dict() if use_cache else None

        self.cosmology = FlatLambdaCDM(**cosmology)
        self.halo_mass_def = halo_mass_def
        self.lightcone = bool(lightcone)
        self.sky_area  = float(sky_area)

        _c = 299792.458
        _abs_mask_func = lambda x: np.where(x==99.0, np.nan, x + 5 * np.log10(self.cosmology.h))
        _mask_func = lambda x: np.where(x==99.0, np.nan, x)

        self._quantity_modifiers = {
            'redshift': 'truth/Z_RSD',
            'ra_true': 'truth/RA',
            'dec_true': 'truth/DEC',
            'redshift_true' : 'truth/Z'
        }
    
    def _generate_native_quantity_list(self):
        native_quantities = set()
        for subset in self._catalog_path_template.keys():
            f = self._open_dataset(subset)
            for name, (dt, size) in f.data.dtype.fields.items():
                if dt.shape:
                    for i in range(dt.shape[0]):
                        native_quantities.add('/'.join((subset, name, str(i))))
                else:
                    native_quantities.add('/'.join((subset, name)))
        return native_quantities


    def _iter_native_dataset(self, native_filters=None):
        assert not native_filters, '*native_filters* is not supported'
        yield functools.partial(self._native_quantity_getter)


    def _open_dataset(self, subset):
        path = self._catalog_path_template[subset]

        if self.cache is None:
            return FitsFile(path)

        key = (subset)
        if key not in self.cache:
            self.cache[key] = FitsFile(path)
        return self.cache[key]


    def _native_quantity_getter(self, native_quantity):
        native_quantity = native_quantity.split('/')
        assert len(native_quantity) in {2,3}, 'something wrong with the native_quantity {}'.format(native_quantity)
        subset = native_quantity.pop(0)
        column = native_quantity.pop(0)
        data = self._open_dataset(subset).data[column]

        if native_quantity:
            data = data[:,int(native_quantity.pop(0))]

        print(data)

        return data
