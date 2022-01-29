import sqlite3
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from biz_logic import get_int_rate_sw


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect('fss_scenario.db')
cursor = conn.cursor()

@app.get('/')
async def calucate(
  base_date: str = None,
  currency: str = None,
  ltfr: float = None,
  spread: float = None,
  llp: float = None,
  cp: float = None,
  freq: int = None,
  tenor0: str = None,
  shock_cont: str = None
):
    alpha0 = 0.1
    t = 1200
    sql = """
    SELECT BASE_DATE, TENOR, YIELD_RATE
      FROM YIELD_RATE_HIST
      WHERE BASE_DATE = (SELECT MAX(BASE_DATE) FROM YIELD_RATE_HIST WHERE BASE_DATE <= ? AND CURRENCY = ?)
        AND CURRENCY = ?
        ORDER BY TENOR
    """
    
    cursor.execute(sql, (base_date, currency, currency))
    result = cursor.fetchall()
    base_date_aply = result[0][0]
    tenor2ytm = {k: v for (_, k, v) in result}
    tenor0 = np.array(eval(tenor0))
    ytm = np.array([tenor2ytm[k] for k in tenor0])
    shock_cont = np.array(eval(shock_cont)[:len(tenor0[tenor0<=llp])])
    int_rate_sw = get_int_rate_sw(tenor0, ytm, shock_cont, alpha0, ltfr, freq, spread, cp, 1e-4, llp, t)

    int_rate_sw_all = dict(
      data=int_rate_sw,
      info=dict(
        baseDate=base_date_aply,
        currency=currency,
        tenor0=tenor0.tolist(),
        ytm=ytm.tolist(),
        shockCont=shock_cont.tolist(),
        ltfr=ltfr,
        spread=spread,
        llp=llp,
        cp=cp,
        freq=freq
      )
    )

    return int_rate_sw_all