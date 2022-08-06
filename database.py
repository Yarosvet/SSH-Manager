from db.db_session import create_session
from db.connections import Connection
from os import path, mkdir, remove
from shutil import copy


class Database:
    def get_dict(self):
        res = {}
        with create_session() as session:
            l = list(sorted(list(session.query(Connection)), key=lambda x: x.id))
        for i in range(len(l)):
            res["[{}] {}".format(i + 1, l[i].name)] = l[i].id
        return res

    def get_by_id(self, e_id: int) -> Connection:
        with create_session() as session:
            return session.query(Connection).get(e_id)

    def get_newrow_id(self):
        with create_session() as session:
            o = Connection()
            session.add(o)
            session.flush()
            session.refresh(o)
            return o.id

    def register_pem(self, pem_path, e_id):
        with create_session() as session:
            e = session.query(Connection).get(e_id)
            if path.exists("data/pem/{}.pem".format(e.id)):
                remove("data/pem/{}.pem".format(e.id))
            copy(pem_path, "data/pem/{}.pem".format(e.id))
            e.pem = "data/pem/{}.pem".format(e.id)
            session.commit()

    def add_connection_pem(self, name: str, ip: str, port: int, pem_path: str):
        if not path.exists("data/pem/"):
            mkdir("data/pem")
        with create_session() as session:
            conn = Connection(name=name, ip=ip, port=port, auth="pem")
            session.add(conn)
            session.commit()
            session.refresh(conn)
            self.register_pem(pem_path=pem_path, e_id=conn.id)

    def add_connection_password(self, name: str, ip: str, port: int, user: str, password: str):
        with create_session() as session:
            conn = Connection(name=name, ip=ip, port=port, auth="password", user=user, password=password)
            session.add(conn)
            session.commit()

    def edit_connection(self, e_id, name=None, ip=None, port=None, auth=None, pem=None, user=None, password=None):
        with create_session() as session:
            e = session.query(Connection).get(e_id)
            if not e:
                return
            if name:
                e.name = name
            if ip:
                e.ip = ip
            if port:
                e.port = port
            if auth:
                e.auth = auth
            if pem:
                self.register_pem(pem_path=pem, e_id=e_id)
            if user:
                e.user = user
            if password:
                e.password = password
            session.commit()
