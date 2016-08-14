import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    hostname = Column(String)
    port = Column(Integer)
    username = Column(String)
    ip = Column(String)
    description = Column(String)

    def __repr__(self):
        return "<Device(hostname='%s', port='%d', username='%s',"\
               "ip='%s', description='%s'" % (
               self.hostname, self.port, self.username,
               self.ip, self.description)

class ConfigDatabase:
    """
    Defines an instance of the go configuration
    database.
    """
    
    def __init__(self, dbname=None):
        """
        :param dbname: sqlite database
        """
        if dbname is None:
            dbhome = '{}/.go'.format(os.path.expanduser('~'))
            if not os.path.exists(dbhome):
                os.makedirs(dbhome)
                self.configdb = '{}/.configdb'.format(dbhome)
        else:
            self.configdb = dbname
        self.engine = create_engine('sqlite:///' + self.configdb, echo=False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def update_new_entry(self, hostname, port, username, ip,
                          description=None):
        device = Device(hostname=hostname,
                        port=port,
                        username=username,
                        ip=ip,
                        description=description or '')

        self.session.add(device)
        self.session.commit()

    def remove_entry(self, hostname):
        device = self.session.query(Device).first()
        self.session.delete(device)
        self.session.commit()

    def lookup_id(self, id):
        user =  self.session.query(Device).filter(Device.id == id).first()
        return user

    def lookup_entry(self, hostname):
        user = self.session.query(Device).filter(
                Device.hostname == hostname).first()
        return user

    def print_config_db(self):
        """
        Print the contents of the database as a menu
        :return: none
        """
        for row in self.session.query(Device):
            print(str(row.id) + ") " + row.hostname)
        print("\n")

    def update_with_config(self, config):
        """
        Bulk load from config csv file
        :param config: str
        :return: none
        """
        with open(config, 'r') as fp:
            config_data = fp.read()
        recs = 0
        errs = 0
        for line in config_data.split('\n'):
            if not line:
                continue
            try:
                hostname, port, username, ipaddress, desc = line.split(',')
                self.update_new_entry(hostname, port, username,
                                      ipaddress, desc)
                recs += 1
            except:
                errs += 1
                continue
        print("[*] Inserted {} records".format(recs))
        if errs > 0:
            raise Exception('[*] Errors on insert %d' % errs)
        
