import pymysql

# Permitir que Django trabaje con PyMySQL simulando mysqlclient
pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()
