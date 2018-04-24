"""
MXXL galaxy catalog class.
"""
from __future__ import division
import os
import re
import numpy as np
import h5py
from astropy.cosmology import FlatLambdaCDM
from GCR import BaseGenericCatalog


__all__ = ['MXXLGalaxyCatalog']


class MXXLGalaxyCatalog(BaseGenericCatalog):
    """
    MXXL galaxy catalog class. Uses generic quantity and filter mechanisms
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
            'galaxy_id' :         'mxxl_id',
            'ra_true':            'ra',
            'dec_true':           'dec',
            'redshift':           'z_obs',
            'redshift_true':      'z_cos',
            'halo_mass':          (lambda x : x / self.cosmology.h, 'halo_mass'),
            'is_central':         (lambda x : (x==0) | (x==2), 'galaxy_type'),
        }

        self._quantity_modifiers['mag_r_sdss'] = 'app_mag'
        self._quantity_modifiers['Mag_r_sdss'] = (lambda x : x + 5*np.log10(self.cosmology.h), 'abs_mag')
        self._quantity_modifiers['Mag_g_sdss'] = (lambda x, y : x + y + 5*np.log10(self.cosmology.h), 'g_r', 'abs_mag')

        self._quantity_modifiers['is_BGS'] = (lambda x: np.zeros_like(x, dtype=np.bool), 'ra')
        self._quantity_modifiers['is_LRG'] = (lambda x: np.zeros_like(x, dtype=np.bool), 'ra')
        self._quantity_modifiers['is_ELG'] = (lambda x: np.zeros_like(x, dtype=np.bool), 'ra')
        self._quantity_modifiers['is_QSO'] = (lambda x: np.zeros_like(x, dtype=np.bool), 'ra')
        
        galtype = re.search(r'/([BGSLREQO]{3})_', self._file).group(1).upper()
        self._quantity_modifiers['is_{}'.format(galtype)] = (lambda x: np.ones_like(x, dtype=np.bool), 'ra')


    def _generate_native_quantity_list(self):
        with h5py.File(self._file, 'r') as fh:
            hgroup = fh['Data']
            hobjects = []
            #get all the names of objects in this tree
            hgroup.visit(hobjects.append)
            #filter out the group objects and keep the dataste objects
            hdatasets = [hobject for hobject in hobjects if type(hgroup[hobject]) == h5py.Dataset]
            native_quantities = set(hdatasets)
        return native_quantities


    def _iter_native_dataset(self, native_filters=None):
        assert not native_filters, '*native_filters* is not supported'
        with h5py.File(self._file, 'r') as fh:
            def native_quantity_getter(native_quantity):
                return fh['Data/{}'.format(native_quantity)].value
            yield native_quantity_getter
