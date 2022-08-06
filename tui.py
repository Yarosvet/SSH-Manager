import npyscreen
from config import *
from database import Database


class App(npyscreen.StandardApp):
    def onStart(self):
        self.database = Database()
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.addForm("MAIN", MenuForm, name="SSH Connection manager ver. {}".format(version))
        self.addForm("CONNECTIONS", ConnectionsForm)
        self.addForm("ADDCONNPASS", AddConnFormPass)
        self.addForm("ADDCONNPEM", AddConnFormPem)
        self.addForm("INVALIDPORTPEM", InvalidPortPem)
        self.addForm("INVALIDPORTPASS", InvalidPortPassword)
        self.addForm("FILEUNSET", FileUnset)


class MenuForm(npyscreen.FormBaseNew):
    def create(self):
        self.list_actions = self.add(npyscreen.MultiLineAction, values=list(self.menu_elements.keys()))
        self.list_actions.actionHighlighted = self.handle_select

    def handle_select(self, act_on_this, key_press):
        self.menu_elements[act_on_this](self)

    def go_connections(self):
        self.parentApp._Forms["CONNECTIONS"].update_fields()
        self.parentApp.switchForm("CONNECTIONS")

    def go_addconnpass(self):
        self.parentApp._Forms["ADDCONNPASS"].update_fields()
        self.parentApp.switchForm("ADDCONNPASS")

    def go_addconnpem(self):
        self.parentApp._Forms["ADDCONNPEM"].update_fields()
        self.parentApp.switchForm("ADDCONNPEM")

    def on_exit(self):
        exit(0)

    menu_elements = {"Connections (Press [E] to edit connection)": go_connections,
                     "Add connection using password": go_addconnpass,
                     "Add connection using PEM file": go_addconnpem,
                     "Exit": on_exit}


class ConnectionsForm(npyscreen.FormBaseNew):
    def create(self):
        self.enum_dict = self.parentApp.database.get_dict()
        self.enum_dict["Back"] = -1
        self.list_conn = self.add(npyscreen.MultiLineAction,
                                  values=list(sorted(self.enum_dict.keys(), key=lambda x: self.enum_dict[x])))
        self.list_conn.add_handlers({"e": self.e_pressed})
        self.list_conn.actionHighlighted = self.handle_select

    def update_fields(self):
        self.enum_dict = self.parentApp.database.get_dict()
        self.enum_dict["Back"] = -1
        self.list_conn.values = list(sorted(self.enum_dict.keys(), key=lambda x: self.enum_dict[x]))

    def handle_select(self, act_on_this, key_press):
        e_id = self.enum_dict[act_on_this]
        if e_id == -1:
            self.parentApp.switchForm("MAIN")
        else:
            pass  # Todo: connect to host

    def e_pressed(self, _input):

        pass  # Todo: edit connection


class AddConnFormPass(npyscreen.FormBaseNew):
    def create(self):
        self.add_handlers({"^X": self.cancel_handler})
        self.name_box = self.add(npyscreen.TitleText, name="Name",
                                 value="Connection #{}".format(self.parentApp.database.get_newrow_id()))
        self.ip_box = self.add(npyscreen.TitleText, name="IP address")
        self.port_box = self.add(npyscreen.TitleText, name="Port", value="22")
        self.user_box = self.add(npyscreen.TitleText, name="User", value="root")
        self.password_box = self.add(npyscreen.TitlePassword, name="Password")
        self.save_button = self.add(npyscreen.ButtonPress, name="Save", relx=12)
        self.cancel_button = self.add(npyscreen.ButtonPress, name="Cancel", rely=self.save_button.rely,
                                      relx=self.save_button.relx + 11)
        self.save_button.whenPressed = self.save_handler
        self.cancel_button.whenPressed = self.cancel_handler

    def update_fields(self):
        self.name_box.value = "Connection #{}".format(self.parentApp.database.get_newrow_id())

    def save_handler(self):
        if not self.port_box.value.isdigit():
            self.parentApp.switchForm("INVALIDPORTPASS")
            return
        port = int(self.port_box.value)
        self.parentApp.database.add_connection_password(name=self.name_box.value, ip=self.ip_box.value, port=port,
                                                        user=self.user_box.value, password=self.password_box.value)
        self.parentApp.switchForm("MAIN")

    def cancel_handler(self, _input=None):
        self.parentApp.switchForm("MAIN")


class AddConnFormPem(npyscreen.FormBaseNew):
    def create(self):
        self.add_handlers({"^X": self.cancel_handler})
        self.name_box = self.add(npyscreen.TitleText, name="Name",
                                 value="Connection #{}".format(self.parentApp.database.get_newrow_id()))
        self.ip_box = self.add(npyscreen.TitleText, name="IP address")
        self.port_box = self.add(npyscreen.TitleText, name="Port", value="22")
        self.pemfile_box = self.add(npyscreen.TitleFilenameCombo, name="PEM file")
        self.save_button = self.add(npyscreen.ButtonPress, name="Save", relx=12)
        self.cancel_button = self.add(npyscreen.ButtonPress, name="Cancel", rely=self.save_button.rely,
                                      relx=self.save_button.relx + 11)
        self.save_button.whenPressed = self.save_handler
        self.cancel_button.whenPressed = self.cancel_handler

    def update_fields(self):
        self.name_box.value = "Connection #{}".format(self.parentApp.database.get_newrow_id())
        self.pemfile_box.value = None

    def save_handler(self):
        if not self.port_box.value.isdigit():
            self.parentApp.switchForm("INVALIDPORTPEM")
            return
        if self.pemfile_box.value is None:
            self.parentApp.switchForm("FILEUNSET")
            return
        port = int(self.port_box.value)
        self.parentApp.database.add_connection_pem(name=self.name_box.value, ip=self.ip_box.value, port=port,
                                                   pem_path=self.pemfile_box.value)
        self.parentApp.switchForm("MAIN")

    def cancel_handler(self, _input=None):
        self.parentApp.switchForm("MAIN")


class InvalidPortPem(npyscreen.FormBaseNew):
    DEFAULT_LINES = 5
    DEFAULT_COLUMNS = 24
    SHOW_ATX = 10
    SHOW_ATY = 2

    def create(self):
        y, x = self.parentApp._Forms["ADDCONNPEM"].useable_space()
        self.name = "Invalid port number"
        self.SHOW_ATX = (x - self.DEFAULT_COLUMNS) // 2
        self.SHOW_ATY = (y - self.DEFAULT_LINES) // 2
        self.button_ok = self.add(npyscreen.ButtonPress, name="OK", relx=self.useable_space()[1] // 2 - 2)
        self.button_ok.whenPressed = self.ok_pressed

    def ok_pressed(self):
        self.parentApp.switchForm("ADDCONNPEM")


class FileUnset(npyscreen.FormBaseNew):
    DEFAULT_LINES = 5
    DEFAULT_COLUMNS = 26
    SHOW_ATX = 10
    SHOW_ATY = 2

    def create(self):
        y, x = self.parentApp._Forms["ADDCONNPEM"].useable_space()
        self.name = "PEM file not selected"
        self.SHOW_ATX = (x - self.DEFAULT_COLUMNS) // 2
        self.SHOW_ATY = (y - self.DEFAULT_LINES) // 2
        self.button_ok = self.add(npyscreen.ButtonPress, name="OK", relx=self.useable_space()[1] // 2 - 2)
        self.button_ok.whenPressed = self.ok_pressed

    def ok_pressed(self):
        self.parentApp.switchForm("ADDCONNPEM")


class InvalidPortPassword(npyscreen.FormBaseNew):
    DEFAULT_LINES = 5
    DEFAULT_COLUMNS = 24
    SHOW_ATX = 10
    SHOW_ATY = 2

    def create(self):
        y, x = self.parentApp._Forms["ADDCONNPASS"].useable_space()
        self.name = "Invalid port number"
        self.SHOW_ATX = (x - self.DEFAULT_COLUMNS) // 2
        self.SHOW_ATY = (y - self.DEFAULT_LINES) // 2
        self.button_ok = self.add(npyscreen.ButtonPress, name="OK", relx=self.useable_space()[1] // 2 - 2)
        self.button_ok.whenPressed = self.ok_pressed

    def ok_pressed(self):
        self.parentApp.switchForm("ADDCONNPASS")
