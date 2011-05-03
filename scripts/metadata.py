from excel import ExcelDictReader
from geonode.maps.models import Layer
from decimal import Decimal

def update(filename):
    reader = ExcelDictReader(filename, 0, 11, 12)
    layer_names = Layer.objects.values_list('name', flat=True)
    for row in reader:
        v = Layer.objects.filter(name=row['layer_name']).update(
                                 title = row['title_en'],
                                 abstract = row['abstract_en'],
                                 date = row['date'] or None,
                                    )

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print 'Usage: python metadata.py haitimetadata.xls'
        sys.exit(-1)
    update(sys.argv[1])
