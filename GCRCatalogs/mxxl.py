"""
Alpha Q galaxy catalog class.
"""
from __future__ import division
import os
import numpy as np
import h5py
from astropy.cosmology import FlatLambdaCDM
from GCR import BaseGenericCatalog
import re

__all__ = ['AlphaQGalaxyCatalog', 'AlphaQClusterCatalog']


class MXXLGalaxyCatalog(BaseGenericCatalog):
    """
    MXXL galaxy catalog class. Uses generic quantity and filter mechanisms
    defined by BaseGenericCatalog class.
    """

    def _subclass_init(self, filename, cosmology=None, metadata=None, **kwargs):

        assert os.path.isfile(filename), 'Catalog file {} does not exist'.format(filename)
        self._file = filename
        self.lightcone = kwargs.get('lightcone')

        try:
            catalog_version = '{}.{}'.format(
                metadata['versionMajor'],
                metadata['versionMinor'],
            )
        except KeyError:
            #If no version is specified, it's version 2.0
            catalog_version = '1.0'

        self.cosmology = FlatLambdaCDM(
                H0=cosmology['H_0'],
                Om0=cosmology['Omega_matter'],
                Ob0=cosmology['Omega_b']
            )

        config_version = kwargs.get('version', '')
        if config_version != catalog_version:
            raise ValueError('Catalog file version {} does not match config version {}'.format(catalog_version, config_version))

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
        self._quantity_modifiers['is_BGS'] = (lambda x: False*x, 'ra') 
        self._quantity_modifiers['is_LRG'] = (lambda x: False*x, 'ra') 
        self._quantity_modifiers['is_ELG'] = (lambda x: False*x, 'ra') 
        self._quantity_modifiers['is_QSO'] = (lambda x: False*x, 'ra') 
        name = self._init_kwargs['filename']
        regex=re.compile(r"^.*/(.*)_[^_]*$")
        galtype = re.sub(regex,r"\1",name)
        self._quantity_modifiers['is_{}'.format(galtype.upper())] = (lambda x: 0*x+True, 'ra')



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

    def _get_native_quantity_info_dict(self, quantity, default=None):
        raise(NotImplementedError)

    def _get_quantity_info_dict(self, quantity, default=None):
        return default
        #TODO needs some fixing
        # print "in get quantity"
        # native_name = None
        # if quantity in self._quantity_modifiers:
        #     print "in quant modifers"
        #     q_mod = self._quantity_modifiers[quantity]
        #     if isinstance(q_mod,(tuple,list)):
        #         print "it's a list object, len:",len(length)

        #         if(len(length) > 2):
        #             return default #This value is composed of a function on
        #             #native quantities. So we have no idea what the units are
        #         else:
        #             #Note: This is just a renamed column.
        #             return self._get_native_quantity_info_dict(q_mod[1],default)
        #     else:
        #         print "it's a string: ",q_mod
        #         return self._get_native_quantity_info_dict(q_mod,default)
        # elif quantity in self._native_quantities:
        #     print "in get native quant"
        #     return self._get_native_quantity_info_dict(quantity,default)
