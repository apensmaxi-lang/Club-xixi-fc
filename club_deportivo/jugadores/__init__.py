# Usamos PyMySQL como conector MySQL/MariaDB (se instala fácil en Windows con XAMPP).
import pymysql

pymysql.version_info = (2, 2, 1, "final", 0)  # Django exige mysqlclient >= 2.2.1
pymysql.install_as_MySQLdb()
