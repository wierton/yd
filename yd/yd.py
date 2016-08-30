import ydsearch as yd
import diskcache, dbcache

def fetch_initdata():
    from getpass import getuser
    with open('/home/{}/.yd/.info'.format(getuser())) as fp:
        initinfo = fp.read().split('&')[0]
        if initinfo == 'db':
            return dbcache.search
        elif initinfo == 'disk':
            return diskcache.search
    except:
        return None

def parse_args():
    help  = "yd [options] word\n"
    help += "\n"
    help += "-s, --save-to=[db|disk] "
    help += "designate the place for local cache\n"
    help += "-u, --user=[name]       "
    help += "set the user to access local database\n"
    help += "-p, --password=[passwd] "
    help += "set the password corresponding to the user name\n"
    help += "-h, --help              "
    help += "display the help and exit\n"
    help += "-v, --version           "
    help += "output version information and exit\n"

    import sys, getopts
    opts, args = getopts.getopts(sys.argv[1:], "s:u:p:hv", ['save-to=', 'user=', 'password=', 'help', 'version', 'skip-init'])
    for opt,value in opts:
        if opt in ('-h', '--help'):
            print help
            exit(0)
        elif opt in ('-v', '--version'):
            print 'yd version 0.0.2'
            exit(0)
        elif opt in ('-s', '--save-to'):
            whcache = value
        elif opt in ('-u', '--user='):
            username = value
        elif opt in ('-p', '--password='):
            password = value
        elif opt == '--skip-init':
            skipinit = True

    #if has inited
    handler = fetch_initdata()
    if handler:
        handler(args)
        exit(0)

    #haven't init the cache directory
    if whcache != 'disk' and dbcache.init(username, password):
        pass
    else:
        diskcache.init()


if __name__ == "__main__":
    parse_args()
