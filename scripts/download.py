import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key

AWS_ACCESS_KEY_ID=os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']

conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

bucket = conn.get_bucket('haitidata.org')

rs = bucket.list()

BASE_DIR = '/data/haitidata.org/'

for key in rs:
    file = BASE_DIR + key.name
    (head, tail) = os.path.split(file)
    (root, ext) = os.path.splitext(tail)
    if(os.path.exists(head) == False):
        os.makedirs(head)
    if(len(tail) > 0):
        parts = head.split('/')
        if(os.path.exists(file) ==  False):
            fp = open (file, "w")
            key.get_file(fp)
            print "downloaded " + key.name

