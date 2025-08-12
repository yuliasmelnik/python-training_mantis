import importlib
import pytest
import json
import os.path
import ftputil
from comtypes.client import CreateObject

from fixture.application import Application
from fixture.db import DbFixture
from model.project import Project

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    webadmin_config = config['webadmin']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
        fixture.session.ensure_login(username=webadmin_config['username'], password=webadmin_config['password'])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)

def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")

def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")

@pytest.fixture(scope="session")
def db(request):
    db_config = load_config(request.config.getoption("--target"))['db']
    dbfixture = DbFixture(host=db_config['host'], name=db_config['name'], user=db_config['user'], password=db_config[
        'password'])
    def fin():
        dbfixture.destroy()
        request.addfinalizer(fin)
    return dbfixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("xlsx_"):
            testdata = load_from_xlsx(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])

def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata

def load_from_xlsx(file):
    os.system('python ./generator/projects.py')
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data\\%s.xlsx" % file)
    xl = CreateObject("Excel.Application")
    xl.Visible = 1
    wb = xl.Workbooks.Open(f)
    worksheet = wb.Sheets[1]
    xlsx_projects = []
    for row in range(1, 6):
        name = worksheet.Cells[row, 1].Value()
        status = worksheet.Cells[row, 2].Value()
        status_formatted = "{:f}".format(status).rstrip('0').rstrip('.')
        description = worksheet.Cells[row, 3].Value()
        project = Project(name=name, status=status_formatted, description=description)
        xlsx_projects.append(project)
    xl.Quit()
    return xlsx_projects