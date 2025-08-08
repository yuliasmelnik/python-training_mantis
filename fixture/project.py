class ProjectHelper:


    def __init__(self, app):
        self.app = app

    def open_project_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("manage_proj_page.php")
                and len(wd.find_elements_by_xpath("//option[""@value='Create New Project']") > 0)):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def create(self, project):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        wd.find_element_by_name("name").click()
        wd.find_element_by_name("name").clear()
        wd.find_element_by_name("name").send_keys(project.name)
        wd.find_element_by_name("status").click()
        #wd.find_element_by_name("status").clear()
        #wd.find_element_by_name("status").send_keys(project.status)
        wd.find_element_by_xpath("//select[@name='status']/option[@value='"+project.status+"']").click()
        wd.find_element_by_name("description").click()
        wd.find_element_by_name("description").clear()
        wd.find_element_by_name("description").send_keys(project.description)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.return_to_project_page()

    def return_to_project_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("manage_proj_page.php")
                and len(wd.find_elements_by_xpath("//option[""@value='Create New Project']") > 0)):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()