import glob
import sys

from utilities import GeoNodeException, simple_save

import logging
for _module in ["utilities"]:
    _logger = logging.getLogger(_module)
    _logger.addHandler(logging.StreamHandler())
    _logger.setLevel(logging.DEBUG)

for shp in glob.glob('shp/*.shp'):
    print shp
    try:
        simple_save(shp)
    except:
        print sys.exc_info()

for tif in glob.glob('tif/*.tif'):
    print tif
    try:
        simple_save(tif)
    except:
        print sys.exc_info()

