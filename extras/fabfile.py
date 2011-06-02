from fabric.api import env, local, run, sudo, put
  
def vagrant():
    # change from the default user to 'vagrant'
    env.user = 'vagrant'
    # connect to the port-forwarded ssh
    env.hosts = ['127.0.0.1:2222']

    # use vagrant ssh key
    result = local('vagrant ssh_config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]

def haitidataorg():
    env.hosts = ['ubuntu@haitidata.org']
    env.key_filename = 'geonode-gfdrr-labs.pem'

def install():
    """Install RISIKO and it's dependencies
    """
    run('wget https://github.com/GFDRR-Labs/haitidata/raw/master/scripts/haitidata-install')
    run('bash haitidata-install')
    run('echo "source ~/venv/bin/activate" >> .bash_aliases')
    run('echo "export DJANGO_SETTINGS_MODULE=haitidata.settings" >> .bash_aliases')
    run('echo "export HAITIDATA_HOME=\"pwd ~\"" >> .bash_aliases')
    run('rm haitidata-install')
    run('rm distribute*')

def production():
    """Install and configure Apache and Tomcat
    """
    put('haitidata.apache', 'haitidata.apache')
    sudo('/bin/mv -f haitidata.apache /etc/apache2/sites-available/haitidata')
    sudo('a2dissite default')
    sudo('a2dissite geonode')
    sudo('a2ensite haitidata')
    run('mkdir -p logs')
    pull()
    run('source venv/bin/activate; pip install -r haitidata/extras/requirements.txt')
    run('rm -rf haitidata/haitidata/site_media')
    run('source venv/bin/activate;django-admin.py build_static --noinput')
    run('cd haitidata/haitidata/site_media/static; wget -c http://dev.geonode.org/dev-data/geonode-client.zip; unzip geonode-client.zip')
    #FIXME: Override geonode theme by copying the haitidata folder into theme
    run('cp -rf haitidata/haitidata/media/haitidata/* haitidata/haitidata/site_media/static/theme')


def manual():
    """Manual steps, not everything can be automated, but we try.
    """

    print "Please perform the following manual steps"
    print
    # Step 1
    print "Step 1. Create a superuser to administer Risk in a Box"
    print "        ssh into the production server and run:"
    print "        django-admin.py createsuperuser"


def haitidata():
    """Do a full production setup of Haitidata
    """

    install()
    production()
    manual()

def stop():
    """Stop haitidata
    """

    sudo('service tomcat6 stop')
    sudo('service apache2 stop')
    #FIXME: This can have unintended consecuences shutting down
    # a Java server that is not GeoNode related.
#    sudo('killall -9 java')

def start():
    """Start haitidata
    """

    run('source venv/bin/activate;django-admin.py syncdb --noinput')
    sudo('service tomcat6 start')
    sudo('service apache2 start')

def restart():
    """Restart haitidata
    """

    stop()
    start()

def pull():
    """Pull the latest changes of the codebase from github and reload the server
    """

    run('cd haitidata; git pull')
    run('cd geonode; git pull')
    run('touch haitidata/extras/project.wsgi')

def log():
    """Handy way to check the logs
    """

    GEOSERVER_LOG = 'tomcat/webapps/geoserver-geonode-dev/data/logs/geoserver.log'
    run('tail logs/*')
    run('tail -n 50 %s' % GEOSERVER_LOG)

def dns():
    """Useful when default DNS does not work
    """
    sudo('rm /etc/resolv.conf')
    sudo('echo "nameserver 4.2.2.2" >> /etc/resolv.conf')

def ariel():
    """Setup dev env for Ariel
    """
    put('id_rsa', '.ssh/id_rsa')
    put('id_rsa.pub', '.ssh/id_rsa.pub')
    run('git config --global user.name "Ariel Nunez"')
    run('git config --global user.email ingenieroariel@gmail.com')


def metadata():
    """Update the metadata in batch from a excel file
    """
    put('haitimetadata.xls', 'haitimetadata.xls')
#    put('styles.zip', 'styles.zip')
#    run('rm -rf styles;mkdir styles; unzip styles.zip -d styles')
#    pull()
#    run('source venv/bin/activate; pip install xlrd')
#    run('source venv/bin/activate; python haitidata/scripts/metadata.py haitimetadata.xls')
