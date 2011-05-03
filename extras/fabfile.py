from fabric.api import run, sudo, put, env

# Edit this section if you get tired of writing the parameters on the command line
env.hosts = ['ubuntu@ec2-67-202-8-230.compute-1.amazonaws.com']
env.key_filename = 'geonode-gfdrr-labs.pem'

def install():
    """Install RISIKO and it's dependencies
    """
    sudo('apt-get install -y curl python-virtualenv')
    run('curl https://github.com/GFDRR-Labs/haitidata/raw/master/scripts/haitidata-install | bash')
    run('echo "source ~/venv/bin/activate" >> .bash_aliases')
    run('echo "export DJANGO_SETTINGS_MODULE=haitidata.settings" >> .bash_aliases')

def production():
    """Install and configure Apache and Tomcat
    """
    put('haitidata.apache', 'haitidata.apache')
    sudo('/bin/mv -f haitidata.apache /etc/apache2/sites-available/haitidata')
    sudo('a2dissite default')
    sudo('a2dissite geonode')
    sudo('a2ensite haitidata')
    run('mkdir -p logs')
    #FIXME: Get rid of the need for geoserver_token
    run('echo hola >> geoserver_token')
    restart()

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