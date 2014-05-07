#!/usr/bin/python

import socket
def checkport(host,port):
        ''' this function tested if the host+port is avaiable
        input:
        host: host
        port: tcp port

        output: none. the boolean result successful or not
        '''
        result = False
        try:
                sock = socket.create_connection((host,port),timeout=5)
                result = True
        except socket.error as msg:
                sock = None
        finally:
                if sock is not None:
                        sock.close()
        return result

if __name__ == '__main__':
        for hostinfo in open('hostport.conf','r'):
                host,port,comment=hostinfo.strip().split()
                result = checkport(host,int(port))
                print "Port checking on %s,\t%s\tport %s is " %(host,comment,port) + str ( result)
