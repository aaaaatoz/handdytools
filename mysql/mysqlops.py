
import MySQLdb
import random
import string
import thread
import time

def dbdefinetables(dbhost, username, password, dbname):
    db = MySQLdb.connect(host=dbhost, user=username, passwd=password, db=dbname)
    db.autocommit(True)
    cursor = db.cursor()
    for i in xrange(0,20):
        cursor.execute('DROP TABLE IF EXISTS perftest%d' %i)
        cursor.execute('CREATE TABLE perftest%d (name VARCHAR(50))' %i)
    cursor.close()
    db.close()


def dboperations(dbhost, username, password, dbname, timedelay=1):
    db = MySQLdb.connect(host=dbhost, user=username, passwd=password, db=dbname)
    db.autocommit(True)
    cursor = db.cursor()
    index = 0
    while True:
        time.sleep(timedelay)
        randomString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        randomInt = random.randint(0, 19)
        print "input on %d" %randomInt
        cursor.execute('INSERT INTO perftest%d VALUES ("%s")' %(randomInt, randomString))
        cursor.execute('SELECT COUNT(*) FROM perftest%d' %randomInt)
        if index % 10 == 0:
            cursor.close()
            db.close()
            db = MySQLdb.connect(host=dbhost, user=username, passwd=password, db=dbname)
            db.autocommit(True)
            cursor = db.cursor()
        index += 1
    db.close()

if __name__ == "__main__":
    dbhost='localhost'
    username='root'
    password=''
    dbname='skyfii'
    dbdefinetables(dbhost, username, password, dbname)
    try:
        for index in xrange(0,10):
            thread.start_new_thread(dboperations, (dbhost, username, password, dbname, 1))
    except:
        print "Error: unable to start thread"

    while 1:
        pass

