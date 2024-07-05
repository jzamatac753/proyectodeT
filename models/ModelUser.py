from .entities.User import User


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor() 
            sql = """SELECT identificador, nombre, contrasenha, correo_electronico FROM usuarios 
                    WHERE nombre = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def createUser(self, db, user_aux):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO usuarios(nombre, contrasenha, correo_electronico) VALUES 
                        (%s, %s, %s)"""
            data = (user_aux.username, User.generate_password(user_aux.password), 
                    user_aux.email)
            cursor.execute(sql, data)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        return True


    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, fullname FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
