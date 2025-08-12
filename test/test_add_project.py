from model.project import Project


def test_add_project( app, xlsx_projects, db):
    project = xlsx_projects
    old_projects = db.get_project_list()
    app.project.create(project)
    new_projects = app.soap.get_project_list(username="administrator", password ="root")
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)