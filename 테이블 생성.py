import sqlite3

conn = sqlite3.connect('fss_scenario.db')

sql = """
CREATE TABLE IF NOT EXISTS YIELD_RATE_HIST (
    BASE_DATE TEXT,
    CURRENCY TEXT,
    TENOR NUMERIC,
    YIELD_RATE NUMERIC,
    PRIMARY KEY (BASE_DATE, CURRENCY, TENOR)
)
"""
conn.execute(sql)

sql = """
CREATE TABLE IF NOT EXISTS BASIC_SETTING (
    BASE_YYMM TEXT,
    CURRENCY TEXT,
    LLP NUMERIC,
    CP NUMERIC,
    LP NUMERIC,
    VA NUMERIC,
    LTFR NUMERIC,
    FREQ INTEGER,
    TENOR TEXT,
    PRIMARY KEY (BASE_YYMM, CURRENCY)
)
"""
conn.execute(sql)

conn.close()