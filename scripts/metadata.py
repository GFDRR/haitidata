from excel import ExcelDictReader
from geonode.maps.models import Layer, Contact, User
from decimal import Decimal

def contact(username, name, organization):
    user, __ = User.objects.get_or_create(username=username)
    contact, __ = Contact.objects.get_or_create(user=user, defaults={'name': name, 'organization': organization})
    return contact

def update(filename):
    reader = ExcelDictReader(filename, 0, 10, 12)
    layer_names = Layer.objects.values_list('name', flat=True)
    for row in reader:
        name = row['layer_name']

        if row['layer_ref'] is None:
            sys.exit()

        if name in layer_names:
            v = Layer.objects.get(name=name)
            v.supplemental_information= row['attribut_values']
            v.date = row['date']
            c = contact(row['datasource_shortname'], row['poc_fullname'], row['datasource_fullname'])
            v.poc = c
            try:
                v.save()
                print '>> Updated layer: %s' % name
            except Exception, e:
                print 'Problem saving %s: %s' % ( name, str(e))
        else:
            print '## Not found: %s' % name

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print 'Usage: python metadata.py haitimetadata.xls'
        sys.exit(-1)
    update(sys.argv[1])
