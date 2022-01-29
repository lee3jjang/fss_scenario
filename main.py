import sqlite3
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict
from kics_qis4_scenario import SmithWilsonYTM, SmithWilson_ALPHA, Cont2Discrete, SmithWilson


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

def get_int_rate_sw(
      tenor0: List[float], ytm: List[float],
      shock_cont: List[float], alpha0: float, ltfr: float,
      freq: int, spread: float, cp: float, tol: float, llp: float, t: int
    ) -> Dict[str, List[float]]:
    
    t = np.arange(t+2)
    t_out = t/12
    tenor0 = np.array(tenor0)
    ytm = np.array(ytm)
    shock_cont = np.array(shock_cont)

    # Yield2Spot
    spot_cont = SmithWilsonYTM(ytm[tenor0.argmax()], alpha0, tenor0, ytm, freq, tenor0)[tenor0<=llp]
    tenor = tenor0[tenor0<=llp]
    spot_cont_input = np.log(np.exp(spot_cont+shock_cont)+spread)

    # Liability
    alpha = SmithWilson_ALPHA(ltfr, tenor, spot_cont_input, cp, tol)
    spot_disc_liab = Cont2Discrete(SmithWilson(ltfr, alpha, tenor, spot_cont_input, t_out))
    forward_disc_liab = (1+spot_disc_liab[1:])**t[1:]/(1+spot_disc_liab[:-1])**t[:-1]-1

    # Asset
    spot_disc_asset = Cont2Discrete(SmithWilsonYTM(ytm[tenor0.argmax()], alpha0, tenor0, ytm, freq, t_out))
    forward_disc_asset = (1+spot_disc_asset[1:])**t[1:]/(1+spot_disc_asset[:-1])**t[:-1]-1

    result = dict(
        t=t[:-1].tolist(),
        spot_disc_liab=spot_disc_liab[:-1].tolist(),
        forward_disc_liab=forward_disc_liab.tolist(),
        spot_disc_asset=spot_disc_asset[:-1].tolist(),
        forward_disc_asset=forward_disc_asset.tolist()
    )

    return result

@app.get('/')
async def root(custom_setting: bool = False, base_date: str = None, currency: str = 'KRW'):

    # 수익률 데이터
    sql = """
    SELECT TENOR, YIELD_RATE
      FROM YIELD_RATE_HIST
      WHERE BASE_DATE = ?
        AND CURRENCY = ?
        ORDER BY TENOR
    """
    cursor.execute(sql, (base_date, currency))
    result = np.array(cursor.fetchall())
    tenor2ytm = {k: v for (k, v) in result}
    
    # 설정 데이터
    base_yymm = base_date[:6]
    sql = """
    SELECT LLP, CP, LP, VA, LTFR, FREQ, TENOR
      FROM BASIC_SETTING
      WHERE BASE_YYMM = (
          SELECT MAX(BASE_YYMM)
            FROM BASIC_SETTING
           WHERE BASE_YYMM <= ?
             AND CURRENCY = ?
        )
        AND CURRENCY = ?
    """
    cursor.execute(sql, (base_yymm, currency, currency))
    llp, cp, lp, va, ltfr, freq, tenor0 = cursor.fetchone()
    tenor0 = np.array(eval(tenor0))
    ytm = np.array([tenor2ytm[k] for k in tenor0])
    shock_cont = [0. for k in tenor0[tenor0 <= llp]]
    result = get_int_rate_sw(tenor0, ytm, shock_cont, 0.1, ltfr, freq, va, cp, 1e-4, llp, 1200)

    return result