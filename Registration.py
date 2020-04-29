import re
import pymysql
from hashlib import sha1
from datetime import datetime

prompt = "> "
today = datetime.today().date()


class Dbms(object):

    def __init__(self, *args):
        self.db = pymysql.connect("localhost", "registration", "project")
        self.cursor = self.db.cursor()
        self.cursor.execute("use user")
        if len(args) == 5:
            self.username, self.password, self.email, self.dob, self.name = args
            self.password = Dbms.passcode(self.password)
        else:
            self.username, self.password = args
            self.password = Dbms.passcode(self.password)

    @staticmethod
    def passcode(string):
        password = sha1(string.encode()).hexdigest()
        password = "0x" + password
        return password

    def registering(self):
        try:
            k = re.findall("@", self.email)

            if len(k) == 1:
                if today > datetime.strptime(self.dob, '%Y-%m-%d').date():
                    q = f"insert into registered values('{self.email}',{self.password},'{self.username}','{self.dob}','{self.name}') "
                    self.cursor.execute(q)
                    self.db.commit()
                else:
                    self.closing()
                    return 4
            else:
                self.closing()
                return 1

        except pymysql.err.IntegrityError as ex:
            self.closing()
            if re.search(r'PRIMARY\'$', ex.args[1]):
                return 3
            if re.search(r"email'$", ex.args[1], ):
                return 2

        self.db.close()
        return 0

    def log_in(self):
        self.cursor.execute(
            f"select if({self.password}=(Select password from registered where username='{self.username}'),1,0)")

        if self.cursor.fetchone()[0] == 1:
            self.cursor.execute(f"select email,Dob,name from registered where username='{self.username}'")
            return self.cursor.fetchone()
        else:
            return None

    def closing(self):
        self.db.rollback()
        self.db.close()
