import csv
from geonode.maps.models import Layer


metadatacsv = '/home/ubuntu/haitimetadata.csv'
reader = csv.reader(open(metadatacsv, 'r'),
                        dialect=csv.excel_tab, delimiter=',')

for row in reader:
    # Do not look at the header row
    if row[0] == 'id':
        continue
  

    theid = row[0]
    title = unicode(row[2].decode('utf-8'))
    abstract_en = unicode(row[3].decode('utf-8'))
    abstract_fr = unicode(row[4].decode('utf-8'))

    layer = Layer.objects.get(id=theid)

    layer.title = title
    layer.abstract_en = abstract_en
    layer.abstract = abstract_en
    layer.abstract_fr = abstract_fr

    print "Saving layer %s:%s" % (theid, title)
    layer.save()

print "Saved all layers"
