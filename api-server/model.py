from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, create_engine

engine = create_engine('sqlite:///fss_scenario.db', connect_args={'check_same_thread': False}, echo=False)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

class YieldRateHist(Base):
    __tablename__ = 'YIELD_RATE_HIST'

    BASE_DATE = Column(String, primary_key=True)
    CURRENCY = Column(String, primary_key=True)
    TENOR = Column(Float, primary_key=True)
    YIELD_RATE = Column(Float)

class BasicSetting(Base):
    __tablename__ = 'BASIC_SETTING'

    BASE_YYMM = Column(String, primary_key=True)
    CURRENCY = Column(String, primary_key=True)
    LLP = Column(Float)
    CP = Column(Float)
    LP = Column(Float)
    VA = Column(Float)
    LTFR = Column(Float)
    FREQ = Column(Integer)
    TENOR = Column(String)