from db.db_session import create_session
from db.connections import Connection
from os import path, mkdir
from shutil import copy


class Database:
    def get_dict(self):
        res = {}
        with create_session() as session:
            l = list(sorted(list(session.query(Connection)), key=lambda x: x.id))
        for i in range(len(l)):
            res["[{}] {}".format(i + 1, l[i].name)] = l[i].id
        return res

    def get_by_id(self, e_id: int):
        with create_session() as session:
            return session.query(Connection).get(e_id)

    def get_newrow_id(self):
        with create_session() as session:
            o = Connection()
            session.add(o)
            session.flush()
            session.refresh(o)
            return o.id

    def add_connection_pem(self, name: str, ip: str, port: int, pem_path: str):
        if not path.exists("data/pem/"):
            mkdir("data/pem")
        with create_session() as session:
            conn = Connection(name=name, ip=ip, port=port, auth="pem")
            session.add(conn)
            session.commit()
            session.refresh(conn)
            copy(pem_path, "data/pem/{}.pem".format(conn.id))
            conn.pem = "data/pem/{}.pem".format(conn.id)
            session.commit()

    def add_connection_password(self, name: str, ip: str, port: int, user: str, password: str):
        with create_session() as session:
            conn = Connection(name=name, ip=ip, port=port, auth="password", user=user, password=password)
            session.add(conn)
            session.commit()
