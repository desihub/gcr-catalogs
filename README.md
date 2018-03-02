# GCR Catalogs

This repo hosts the mock galaxy catalogs used by [DESIQA](https://github.com/j-dr/descqa).

On a NERSC machine, all these catalogs can be directly accessed through the "Generic Catalog Reader" (GCR) inferface.
More information about GCR can be found [here](https://github.com/yymao/generic-catalog-reader).

Currently these sets of catalogs are available (**Note that these catalogs are not perfect and will continue to be updated**):

1. Buzzard series: 
   by Joe DeRose, Risa Wechsler, Eli Rykoff et al.
   - `buzzard` (full catalog, DES Y3 area)
   - `buzzard_test` (same as `buzzard` but a small subset for testing purpose)
   - `buzzard_high-res` (higher resolution, smaller sky area)
   - `buzzard_v1.6`
      
Each of the catalogs is specified by a YAML config file, which can be found [here](https://github.com/j-dr/gcr-catalogs/tree/desi/GCRCatalogs/catalog_configs). The galaxy quantities in these catalogs conform to [this schema](https://docs.google.com/document/d/1rUsImkBkjjw82Xa_-3a8VMV6K9aYJ8mXioaRhz0JoqI/edit).

## Use GCRCatalogs under the DESIQA Python environment on NERSC

_Note_: These instructions about Python environment may change in the future. If you encounter issues, please check if there's any updates on these instructions.

### with Jupyter notebooks:

First, [start a NERSC notebook server](https://jupyter-dev.nersc.gov) and open a notebook with a [DESI kernel](https://desi.lbl.gov/trac/wiki/Computing/JupyterAtNERSC). Make sure you add the DESIQA Python enviornment to `sys.path`:

```python
import sys
sys.path.insert(0, '/project/projectdirs/desi/mocks/desiqa/cori/lib/python3.5/site-packages/')
```

### in a terminal:

Activate DESIQA Python environment by running the following on NERSC (needs to be in `bash` or `zsh`):

source /project/projectdirs/desi/software/desi_environment.sh
export PYTHONPATH=/project/projectdirs/desi/mocks/desiqa/cori/lib/python3.5/site-packages/:$PYTHONPATH

### with a python script: 

To be able to import `GCRCatalogs`, make sure you first source the desi environment (source /project/projectdirs/desi/software/desi_environment.sh) and the first line of the script should be:
#!/usr/bin/env python
```python
import sys
sys.path.insert(0, '/project/projectdirs/desi/mocks/desiqa/cori/lib/python3.5/site-packages/')
```

## Install GCRCatalogs on your own

You can install the latest version by running (but note that you need to change the python paths accordingly) 

    pip install https://github.com/j-dr/gcr-catalogs/archive/master.zip

But note that the actual catalogs can only be accessed on a NERSC machine. 


## Usage and examples

- See [this notebook](https://github.com/j-dr/gcr-catalogs/blob/desi/examples/GCRCatalogs%20Demo.ipynb) for a tutorial on how to use GCR Catalogs.

- See [this notebook](https://github.com/j-dr/gcr-catalogs/blob/desi/examples/CLF%20Test.ipynb) for an actual application (the Conditional  Luminosity Function test) using GCR Catalogs. (Thanks to Joe DeRose for providing the CLF test example!)

- See [GCR documentation](https://yymao.github.io/generic-catalog-reader/index.html) for the complete GCR API.


## Contribute to GCRCatalogs:

1. On GitHub [fork](https://guides.github.com/activities/forking/) the GCRCatalogs GitHub repo.

2. On NERSC, clone your fork (you can skip this if you've done it)

       cd /your/own/directory
       git clone git@github.com:YourGitHubUsername/gcr-catalogs.git
       git remote add upstream https://github.com/desihub/gcr-catalogs.git


3. Sync with the upstream master branch

       cd /your/own/directory/gcr-catalogs
       git checkout master
       git pull upstream master
       git push origin master

4. Create a new branch for this edit:

       git checkout -b newBranchName

5. Make changes

6. Test by adding your clone to the path when running Python: 
   ```python
   import sys
   sys.path.insert(0, '/your/own/directory/gcr-catalogs')
   ```

7. Commit and push to your forked repo

       git add <files changed>
       git commit -m <short but meaningful message>
       git push origin newBranchName


8. Go to your forked repo's GitHub page and "create a pull request". 
