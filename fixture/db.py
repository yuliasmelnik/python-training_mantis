import pymysql.cursors
from model.project import Project


class DbFixture:

    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host=host, database=name, user=user, password=password, autocommit=True)

    def get_project_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select id, name, status, description from mantis_project_table")
            for row in cursor:
                (id, name, status, description) = row
                list.append(Project(id=str(id), name=name, status=status, description=description))
        finally:
            cursor.close()
        return list

    def destroy(self):
        self.connection.close()