import logging

from sqlalchemy.ext.automap import automap_base

from sqlalchemy import create_engine

from sqlalchemy import Column
from sqlalchemy import Integer, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.exc import DatabaseError


Base = automap_base()
db_path = 'mysql+mysqlconnector://root:toor@localhost:3306/linker'

class LinkModel(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    origin = Column(Text)
    link = Column(Text)
    title = Column(Text)
    content = Column(LONGTEXT)

    def __repr__(self):
        return f'{self.link}'

    def get_base(self):
        return self.Base


def init_db(db_path, pool_size=None):
    """
    Initialize the database.
    
    :param db_path: The url path to the database.
    :type db_path: str
    """
    try:
        if pool_size:
            engine = create_engine(db_path, pool_size=pool_size, pool_recycle=3600)
        else:
            engine = create_engine(db_path)

        Base.metadata.create_all(engine)
        Base.prepare(engine, reflect=True)
        # linklist = Base.classes.httpsources

    except Exception as e:
        logging.error(e)

    else:
        logging.debug("Database started!")
        return {'engine': engine, 'table': LinkModel}



def bulk_insert(links:list):
    config = init_db(db_path)
    engine = config['engine']
    Table = config['table']
    
    with engine.connect() as connection:
        try:
            connection.execute(Table.__table__.insert(), links)    
        
        except DatabaseError:
            logging.info('Falha ao gravar dados :(')

    return True
