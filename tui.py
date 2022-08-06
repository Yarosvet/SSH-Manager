import npyscreen
from config import *
from database import Database
from os.path import abspath


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
        self.addForm("EDITCONNPEM", EditConnectionPem)
        self.addForm("EDITCONNPASS", EditConnectionPass)
        self.addForm("INVALIDPORTPEMEDIT", InvalidPortPemEdit)
        self.addForm("INVALIDPORTPASSEDIT", InvalidportPasswordEdit)
        self.addForm("FILEUNSETEDIT", FileUnsetEdit)
        self.addForm("DELETECONN", DeleteConnection)
        self.addForm("DELETECONNEDITPASS", DeleteConnectionEditPass)
        self.addForm("DELETECONNEDITPEM", DeleteConnectionEditPem)


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

    menu_elements = {"Connections": go_connections,
                     "Add connection using password": go_addconnpass,
                     "Add connection using PEM file": go_addconnpem,
                     "Exit": on_exit}


class ConnectionsForm(npyscreen.FormBaseNew):
    def create(self):
        self.caption = self.add(npyscreen.FixedText, editable=False,
                                value="Press [E] to edit connection or [DEL] to delete it")
        self.enum_dict = self.parentApp.database.get_dict()
        self.enum_dict["Back"] = -1
        self.list_conn = self.add(npyscreen.MultiLineAction,
                                  values=list(sorted(self.enum_dict.keys(), key=lambda x: self.enum_dict[x])),
                                  rely=self.caption.rely + 2)
        self.list_conn.add_handlers({"e": self.e_pressed, 330: self.delete_pressed})
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
        e_id = self.enum_dict[self.list_conn.values[self.list_conn.cursor_line]]
        e = self.parentApp.database.get_by_id(e_id)
        if not e:
            return
        if e.auth == "pem":
            self.parentApp._Forms["EDITCONNPEM"].set_conn_id(e_id)
            self.parentApp._Forms["EDITCONNPEM"].update_fields()
            self.parentApp.switchForm("EDITCONNPEM")
        elif e.auth == "password":
            self.parentApp._Forms["EDITCONNPASS"].set_conn_id(e_id)
            self.parentApp._Forms["EDITCONNPASS"].update_fields()
            self.parentApp.switchForm("EDITCONNPASS")

    def delete_pressed(self, _input):
        e_id = self.enum_dict[self.list_conn.values[self.list_conn.cursor_line]]
        self.parentApp._Forms["DELETECONN"].editw = 0
        self.parentApp._Forms["DELETECONN"].set_conn_id(e_id)
        self.parentApp.switchForm("DELETECONN")


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
    DEFAULT_LINES = 7
    DEFAULT_COLUMNS = 25
    SHOW_ATX = 10
    SHOW_ATY = 2

    def create(self):
        self.caption = self.add(npyscreen.FixedText, value="Invalid port number", editable=False)
        self.button_ok = self.add(npyscreen.ButtonPress, name="OK", relx=self.useable_space()[1] // 2 - 3,
                                  rely=self.caption.rely + 2)
        self.button_ok.whenPressed = self.ok_pressed

    def ok_pressed(self):
        self.parentApp.switchForm("ADDCONNPEM")


class InvalidPortPemEdit(InvalidPortPem):
    def create(self):
        super().create()
        self.button_ok.whenPressed = self.ok_pressed

    def ok_pressed(self):
        self.parentApp.switchForm("EDITCONNPEM")


class FileUnset(npyscreen.FormBaseNew):
    DEFAULT_LINES = 7
    DEFAULT_COLUMNS = 30
    SHOW_ATX = 10
    SHOW_ATY = 2

    def create(self):
        self.caption = self.add(npyscreen.FixedText, value="PEM file is not selected", editable=False)
        self.button_ok = self.add(npyscreen.ButtonPress, name="OK", relx=self.useable_space()[1] // 2 - 3,
                                  rely=self.caption.rely + 2)
        self.button_ok.whenPressed = self.ok_pressed

    def ok_pressed(self):
        self.parentApp.switchForm("ADDCONNPEM")


class FileUnsetEdit(FileUnset):
    def create(self):
        super().create()
        self.button_ok.whenPressed = self.ok_pressed

    def ok_pressed(self):
        self.parentApp.switchForm("EDITCONNPEM")


class InvalidPortPassword(npyscreen.FormBaseNew):
    DEFAULT_LINES = 7
    DEFAULT_COLUMNS = 25
    SHOW_ATX = 10
    SHOW_ATY = 2

    def create(self):
        self.caption = self.add(npyscreen.FixedText, value="Invalid port number", editable=False)
        self.button_ok = self.add(npyscreen.ButtonPress, name="OK", relx=self.useable_space()[1] // 2 - 3,
                                  rely=self.caption.rely + 2)
        self.button_ok.whenPressed = self.ok_pressed

    def ok_pressed(self):
        self.parentApp.switchForm("ADDCONNPASS")


class InvalidportPasswordEdit(InvalidPortPassword):
    def create(self):
        super().create()
        self.button_ok.whenPressed = self.ok_pressed

    def ok_pressed(self):
        self.parentApp.switchForm("EDITCONNPASS")


class EditConnectionPem(npyscreen.FormBaseNew):
    def set_conn_id(self, conn_id):
        self.conn_id = conn_id

    def create(self):
        self.conn_id = None
        self.add_handlers({"^X": self.cancel_handler})
        self.name_box = self.add(npyscreen.TitleText, name="Name")
        self.ip_box = self.add(npyscreen.TitleText, name="IP address")
        self.port_box = self.add(npyscreen.TitleText, name="Port")
        self.pemfile_box = self.add(npyscreen.TitleFilenameCombo, name="PEM file")
        self.delete_button = self.add(npyscreen.ButtonPress, name="Delete connection", color='BLACK_YELLOW')
        self.delete_button.whenPressed = self.delete_handler
        self.save_button = self.add(npyscreen.ButtonPress, name="Save", relx=12)
        self.cancel_button = self.add(npyscreen.ButtonPress, name="Cancel", rely=self.save_button.rely,
                                      relx=self.save_button.relx + 11)
        self.save_button.whenPressed = self.save_handler
        self.cancel_button.whenPressed = self.cancel_handler

    def update_fields(self):
        e = self.parentApp.database.get_by_id(self.conn_id)
        if not e:
            return
        self.name_box.value = e.name
        self.ip_box.value = e.ip
        self.port_box.value = str(e.port)
        self.pemfile_box.value = abspath(e.pem)

    def delete_handler(self):
        self.parentApp._Forms["DELETECONNEDITPEM"].editw = 0
        self.parentApp._Forms["DELETECONNEDITPEM"].set_conn_id(self.conn_id)
        self.parentApp.switchForm("DELETECONNEDITPEM")

    def save_handler(self):
        if not self.port_box.value.isdigit():
            self.parentApp.switchForm("INVALIDPORTPEMEDIT")
            return
        if self.pemfile_box.value is None:
            self.parentApp.switchForm("FILEUNSETEDIT")
            return
        e = self.parentApp.database.get_by_id(self.conn_id)
        if not e:
            return
        port = int(self.port_box.value)
        new_pem = None
        if self.pemfile_box.value != abspath(e.pem):
            new_pem = self.pemfile_box.value
        self.parentApp.database.edit_connection(e.id, name=self.name_box.value, ip=self.ip_box.value, port=port,
                                                pem=new_pem)
        self.parentApp.switchForm("CONNECTIONS")

    def cancel_handler(self, _input=None):
        self.parentApp.switchForm("CONNECTIONS")


class EditConnectionPass(npyscreen.FormBaseNew):
    def set_conn_id(self, conn_id):
        self.conn_id = conn_id

    def create(self):
        self.conn_id = None
        self.add_handlers({"^X": self.cancel_handler})
        self.name_box = self.add(npyscreen.TitleText, name="Name")
        self.ip_box = self.add(npyscreen.TitleText, name="IP address")
        self.port_box = self.add(npyscreen.TitleText, name="Port")
        self.user_box = self.add(npyscreen.TitleText, name="User")
        self.password_box = self.add(npyscreen.TitlePassword, name="Password")
        self.delete_button = self.add(npyscreen.ButtonPress, name="Delete connection", color='CAUTION')
        self.delete_button.whenPressed = self.delete_handler
        self.save_button = self.add(npyscreen.ButtonPress, name="Save", relx=12)
        self.cancel_button = self.add(npyscreen.ButtonPress, name="Cancel", rely=self.save_button.rely,
                                      relx=self.save_button.relx + 11)
        self.save_button.whenPressed = self.save_handler
        self.cancel_button.whenPressed = self.cancel_handler

    def update_fields(self):
        e = self.parentApp.database.get_by_id(self.conn_id)
        if not e:
            return
        self.name_box.value = e.name
        self.ip_box.value = e.ip
        self.port_box.value = str(e.port)
        self.user_box.value = e.user
        self.password_box.value = e.password

    def delete_handler(self):
        self.parentApp._Forms["DELETECONNEDITPASS"].editw = 0
        self.parentApp._Forms["DELETECONNEDITPASS"].set_conn_id(self.conn_id)
        self.parentApp.switchForm("DELETECONNEDITPASS")

    def save_handler(self):
        if not self.port_box.value.isdigit():
            self.parentApp.switchForm("INVALIDPORTPASSEDIT")
            return
        e = self.parentApp.database.get_by_id(self.conn_id)
        if not e:
            return
        port = int(self.port_box.value)
        self.parentApp.database.edit_connection(e.id, name=self.name_box.value, ip=self.ip_box.value, port=port,
                                                user=self.user_box.value, password=self.password_box.value)
        self.parentApp.switchForm("CONNECTIONS")

    def cancel_handler(self, _input=None):
        self.parentApp.switchForm("CONNECTIONS")


class DeleteConnection(npyscreen.FormBaseNew):
    DEFAULT_LINES = 7
    DEFAULT_COLUMNS = 40
    SHOW_ATX = 10
    SHOW_ATY = 2

    def set_conn_id(self, conn_id):
        self.conn_id = conn_id

    def create(self):
        self.conn_id = None
        self.caption = self.add(npyscreen.FixedText, value="Are you sure to remove connection?", editable=False)
        self.button_no = self.add(npyscreen.ButtonPress, name="No", relx=3, rely=self.caption.rely + 2)
        self.button_no.whenPressed = self.no_pressed
        self.button_yes = self.add(npyscreen.ButtonPress, name="Yes", relx=28,
                                   rely=self.button_no.rely)
        self.button_yes.whenPressed = self.yes_pressed

    def yes_pressed(self):
        if self.conn_id:
            self.parentApp.database.delete_connection(e_id=self.conn_id)
            self.parentApp._Forms["CONNECTIONS"].update_fields()
            self.parentApp.switchForm("CONNECTIONS")

    def no_pressed(self):
        self.parentApp._Forms["CONNECTIONS"].update_fields()
        self.parentApp.switchForm("CONNECTIONS")


class DeleteConnectionEditPass(DeleteConnection):
    def create(self):
        super().create()
        self.button_no.whenPressed = self.no_pressed

    def no_pressed(self):
        self.parentApp.switchForm("EDITCONNPASS")


class DeleteConnectionEditPem(DeleteConnection):
    def create(self):
        super().create()
        self.button_no.whenPressed = self.no_pressed

    def no_pressed(self):
        self.parentApp.switchForm("EDITCONNPEM")
