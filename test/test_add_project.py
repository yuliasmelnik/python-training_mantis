from model.project import Project

def test_add_project(app, db):
    project = Project(name='test_name', status='10', description='test_description')
    old_projects = db.get_project_list()
    app.project.create(project)
    new_projects = db.get_project_list()
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)