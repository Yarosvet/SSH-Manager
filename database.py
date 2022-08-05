from db.db_session import create_session
from db.connections import Connection


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