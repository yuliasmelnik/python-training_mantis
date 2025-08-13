from suds.client import Client
from suds import WebFault

from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_project_list(self, username, password):
        list = []
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            result = client.service.mc_projects_get_user_accessible(username, password)
            for element in result:
                id = element.id
                name = element.name
                status = element.status.id
                description = element.description
                list.append(Project(name=str(name), status=int(status), description=str(description), id=str(id)))
            return list
        except WebFault:
            return False

