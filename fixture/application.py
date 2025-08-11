# -*- coding: utf-8 -*-
from selenium import webdriver
from fixture.james import JamesHelper
from fixture.mail import MailHelper
from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from fixture.signup import SignupHelper


class Application:

    def __init__(self, browser, config):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecoqnized browser %s" % browser)
        self.session = SessionHelper(self)
        self.james = JamesHelper(self)
        self.project = ProjectHelper(self)
        self.signup = SignupHelper(self)
        self.mail = MailHelper(self)
        self.config = config
        self.base_url = config['web']['baseUrl']

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()