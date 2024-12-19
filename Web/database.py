import mysql.connector


class Database():
    def __init__(self,ip,user,passwd,database):
        self.ip = ip
        self.user=user
        self.passwd=passwd
        self.database=database


        

    def add_to_databace(self,query,data):
        try:
            db = mysql.connector.connect(
                host=self.ip,
                user=self.user,
                passwd=self.passwd,
                database=self.database,
                auth_plugin='mysql_native_password'
            )
            cur = db.cursor()
            cur.execute(query,data)
            db.commit()

        except Exception as e:
            return f'encounterd a error: {e}'

        finally:
            db.close()

    def get(self,query,max_output = 20):
        try:
            db = mysql.connector.connect(
                host=self.ip,
                user=self.user,
                passwd=self.passwd,
                database=self.database,
                auth_plugin='mysql_native_password'
            )
            cur = db.cursor()
            cur.execute(query)
            rows = cur.fetchmany(max_output)
            return rows

        except Exception as e:
            print(f'encounterd a error: {e}')

        finally:
            db.close()

    def get_where(self,query,data,max_output = 20):
        try:
            db = mysql.connector.connect(
                host=self.ip,
                user=self.user,
                passwd=self.passwd,
                database=self.database,
                auth_plugin='mysql_native_password'
            )
            cur = db.cursor()
            cur.execute(query,data)
            rows = cur.fetchmany(max_output)
            return rows

        except Exception as e:
            print(f'encounterd a error: {e}')

        finally:
            db.close()

#setup db conection ("ip","user","password,"DBname")
#db = Database("10.136.132.70","lukas","google","test")



#mysql add statment
#øl=("ginis",)
#db.add_to_databace('INSERT INTO goof (øl) VALUES(%s)',øl)


#mysql get
#print(db.get("SELECT * FROM goof"))