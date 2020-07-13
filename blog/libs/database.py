from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from blog import setting

mysql = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(setting['mysql']['username'],
                                                setting['mysql']['password'],
                                                setting['mysql']['host'],
                                                setting['mysql']['port'],
                                                setting['mysql']['db'])
engine = create_engine(mysql, pool_recycle=3600 * 7)

DBSession = sessionmaker(engine)  # 创建DBSession类型
db = scoped_session(DBSession)

Base = declarative_base()
