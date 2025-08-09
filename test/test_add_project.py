from model.project import Project
from comtypes.client import CreateObject
import os

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def test_add_project(app, db):
    file = (os.path.join(project_dir, 'projects.xlsx'))
    xl = CreateObject("Excel.Application")
    xl.Visible = 1
    wb = xl.Workbooks.Open(file)
    worksheet = wb.Sheets[1]
    for row in range(1, 11):
        name = worksheet.Cells[row, 1].Value()
        status = worksheet.Cells[row, 2].Value()
        status_formatted = "{:f}".format(status).rstrip('0').rstrip('.')
        description = worksheet.Cells[row, 3].Value()
        project = Project(name=name, status=status_formatted, description=description)
        old_projects = db.get_project_list()
        app.project.create(project)
        new_projects = db.get_project_list()
        old_projects.append(project)
        assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
    xl.Quit()