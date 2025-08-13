from model.project import Project
import json


def test_add_project( app, xlsx_projects, db):
    project = xlsx_projects
    with open('target.json') as file:
        data = json.load(file)
        username = data['webadmin']['username']
        password = data['webadmin']['password']
    old_projects = app.soap.get_project_list(username=username, password=password)
    app.project.create(project)
    new_projects = app.soap.get_project_list(username=username, password=password)
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)