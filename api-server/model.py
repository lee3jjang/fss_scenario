from urllib.parse import quote
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, VARCHAR, FLOAT, create_engine

# Sqlite
# engine = create_engine('sqlite:///fss_scenario.db', connect_args={'check_same_thread': False}, echo=False)

# Mysql
engine = create_engine(f'mysql+mysqldb://lee3jjang:{quote("1234")}@localhost:3306/fss_scenario', echo=False)
# engine.execute("DROP DATABASE fss_scenario")
# engine.execute("CREATE DATABASE fss_scenario")
# engine.execute("USE fss_scenario")

Base = declarative_base()

class YieldRateHist(Base):
    __tablename__ = 'YIELD_RATE_HIST'

    BASE_DATE = Column(VARCHAR(8), primary_key=True)
    CURRENCY = Column(VARCHAR(3), primary_key=True)
    TENOR = Column(FLOAT, primary_key=True)
    YIELD_RATE = Column(FLOAT)

class BasicSetting(Base):
    __tablename__ = 'BASIC_SETTING'

    BASE_YYMM = Column(VARCHAR(6), primary_key=True)
    CURRENCY = Column(VARCHAR(3), primary_key=True)
    LLP = Column(FLOAT)
    CP = Column(FLOAT)
    LP = Column(FLOAT)
    VA = Column(FLOAT)
    LTFR = Column(FLOAT)
    FREQ = Column(INTEGER)
    TENOR = Column(VARCHAR(150))

Base.metadata.create_all(bind=engine)