from excel import ExcelDictReader
from geonode.maps.models import Layer
from decimal import Decimal
import geoserver
import os

def update(filename):
    reader = ExcelDictReader(filename, 0, 10, 12)
    layer_names = Layer.objects.values_list('name', flat=True)

    cat = Layer.objects.gs_catalog    
    for row in reader:
        name = row['layer_name']

        if row['layer_ref'] is None:
            sys.exit()

        if name in layer_names:
            v = Layer.objects.get(name=name)
            v.title = row['title_en']
            v.abstract = row['abstract_en']
            style_name =  row['style_file']
            style_filename = '/home/ubuntu/styles/%s.sld' % style_name
            print name, style_name
            continue
            if os.path.exists(style_filename):
                f = open(style_filename, 'r')
                style_sld = f.read()
                f.close()
                try:
                    cat.create_style(name,style_sld)
                except geoserver.catalog.ConflictingDataError, e:
                    msg = 'There was already a style named %s in GeoServer, cannot overwrite: "%s"' % (name, str(e))
                    e.args = (msg,)

                publishing = cat.get_layer(name)
                style = cat.get_style(name)
                publishing.default_style = cat.get_style(name)
                cat.save(publishing)

                v.save()
                v.save_to_geonetwork()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print 'Usage: python metadata.py haitimetadata.xls'
        sys.exit(-1)
    update(sys.argv[1])
