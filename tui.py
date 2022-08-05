import npyscreen
from config import *
from database import Database


class App(npyscreen.StandardApp):
    def onStart(self):
        self.database = Database()
        self.addForm("MAIN", MenuForm, name="SSH Connection manager ver. {}".format(version))
        self.addForm("CONNECTIONS", ConnectionsForm)


class MenuForm(npyscreen.FormBaseNew):
    def create(self):
        self.list_actions = self.add(MenuList, values=list(self.menu_elements.keys()))

    def go_connections(self):
        self.parentApp.switchForm("CONNECTIONS")

    menu_elements = {"Connections": go_connections}


class MenuList(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, key_press):
        self.parent.menu_elements[act_on_this](self.parent)


class ConnectionsForm(npyscreen.FormBaseNew):
    def create(self):
        self.enum_dict = self.parentApp.database.get_dict()
        self.enum_dict["Back"] = -1
        lines = list(sorted(self.enum_dict.keys(), key=lambda x: self.enum_dict[x]))
        self.list_conn = self.add(ConnectionsList, values=lines)

    def selected(self, e_id):
        if e_id == -1:
            self.parentApp.switchForm("MAIN")
        else:
            print(e_id)


class ConnectionsList(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, key_press):
        self.parent.selected(self.parent.enum_dict[act_on_this])
