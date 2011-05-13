from excel import ExcelDictReader
from geonode.maps.models import Layer
from decimal import Decimal

def update(filename):
    reader = ExcelDictReader(filename, 0, 11, 12)
    layer_names = Layer.objects.values_list('name', flat=True)
    for row in reader:
        name = row['layer_name']

        if row['layer_ref'] is None:
            sys.exit()

        if name in layer_names:
            v = Layer.objects.get(name=name)
            v.supplemental_information= row['attribut_values']
            print v.supplemental_information
#            v.title = row['title_en']
#            v.abstract = row['abstract_en']
#            v.save()
            print 'Successfully updated layer %s' % name
        else:
            print '%s' % str(name)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print 'Usage: python metadata.py haitimetadata.xls'
        sys.exit(-1)
    update(sys.argv[1])
