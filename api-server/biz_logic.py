import numpy as np
from typing import List, Dict
from kics_qis4_scenario import SmithWilsonYTM, SmithWilson_ALPHA, Cont2Discrete, SmithWilson


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
    disc_fac_liab = 1/(1+spot_disc_liab)**t_out

    # Asset
    spot_disc_asset = Cont2Discrete(SmithWilsonYTM(ytm[tenor0.argmax()], alpha0, tenor0, ytm, freq, t_out))
    forward_disc_asset = (1+spot_disc_asset[1:])**t[1:]/(1+spot_disc_asset[:-1])**t[:-1]-1
    disc_fac_asset = 1/(1+spot_disc_asset)**t_out

    result = dict(
        t=t[:-1].tolist(),
        spotDiscAsset=spot_disc_asset[:-1].tolist(),
        spotDiscLiab=spot_disc_liab[:-1].tolist(),
        forwardDiscAsset=forward_disc_asset.tolist(),
        forwardDiscLiab=forward_disc_liab.tolist(),
        discFacAsset=disc_fac_asset[:-1].tolist(),
        discFacLiab=disc_fac_liab[:-1].tolist(),
    )

    return result