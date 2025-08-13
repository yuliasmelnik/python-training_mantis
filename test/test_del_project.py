import random
import json
from model.project import Project


def test_del_project(app, db):
    with open('target.json') as file:
        data = json.load(file)
        username = data['webadmin']['username']
        password = data['webadmin']['password']
    if len(app.soap.get_project_list(username=username, password=password)) == 0:
        app.project.create(Project(name="test", status="10", description="test"))
    old_projects = app.soap.get_project_list(username=username, password=password)
    project = random.choice(old_projects)
    app.project.delete_project_by_id(project.id)
    new_projects = app.soap.get_project_list(username=username, password=password)
    old_projects.remove(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)