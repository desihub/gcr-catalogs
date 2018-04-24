"""
EZMock galaxy catalog class.
"""
from __future__ import division, print_function
import os
import re
import numpy as np
import pandas as pd
from astropy.cosmology import FlatLambdaCDM
from GCR import BaseGenericCatalog

__all__ = ['EZMockGalaxyCatalog']


class EZMockGalaxyCatalog(BaseGenericCatalog):
    """
    EZmocks galaxy catalog class. Uses generic quantity and filter mechanisms
    defined by BaseGenericCatalog class.
    """

    def _subclass_init(self, filename, **kwargs):

        assert os.path.isfile(filename), 'Catalog file {} does not exist'.format(filename)
        
        self._file = filename
        self.lightcone = kwargs.get('lightcone')
        self.sky_area = float(kwargs.get('sky_area') or 0)
        self.version = kwargs.get('version')        
        self.cosmology = FlatLambdaCDM(**kwargs['cosmology'])

        self._quantity_modifiers = {
            'redshift': 'Z_RSD',
            'ra_true': 'RA',
            'dec_true': 'DEC',
            'redshift_true' : 'Z'
        }
        self._quantity_modifiers['is_BGS'] = (lambda x: np.zeros_like(x, dtype=np.bool), 'RA')
        self._quantity_modifiers['is_LRG'] = (lambda x: np.zeros_like(x, dtype=np.bool), 'RA')
        self._quantity_modifiers['is_ELG'] = (lambda x: np.zeros_like(x, dtype=np.bool), 'RA')
        self._quantity_modifiers['is_QSO'] = (lambda x: np.zeros_like(x, dtype=np.bool), 'RA')

        galtype = re.search(r'_([BGSLREQO]{3})\.', self._file).group(1).upper()
        self._quantity_modifiers['is_{}'.format(galtype)] = (lambda x: np.ones_like(x, dtype=np.bool), 'RA')
        
        self._data = None


    @staticmethod
    def _generate_native_quantity_list():
        return ['RA', 'DEC', 'Z', 'Z_RSD']


    def _native_quantity_getter(self, native_quantity):
        if self._data is None:
            self._data = pd.read_csv(self._file,
                                     delim_whitespace=True,
                                     dtype=np.float64,
                                     names=self._generate_native_quantity_list(),
                                     engine='c',
                                     na_filter=False)
        return self._data[native_quantity].values


    def _iter_native_dataset(self, native_filters=None):
        assert not native_filters, '*native_filters* is not supported'
        yield self._native_quantity_getter
