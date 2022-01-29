import os
import numpy as np


def SmithWilson_ALPHA(ltfr: float, tenor: np.ndarray, spot_cont_input: np.ndarray, cp: float, tol: float) -> float:
    '''Smith-Wilson Alpha 구하는 함수'''

    ALPHA_UB = 1
    ALPHA_LB = 0.001
    ltfr = np.log(1+ltfr)

    n = len(tenor)
    u = tenor.copy()
    P = np.exp(-spot_cont_input*u)
    m = np.exp(-ltfr*u)
    P_M = P-m

    for itr in range(52):
        ALPHA = (ALPHA_UB+ALPHA_LB)*0.5
        S = np.sinh(ALPHA*u)

        W = np.zeros([n, n])
        for i in range(n):
            for j in range(i, n):
                W[i, j] = np.exp(-ltfr*(u[i]+u[j]))*(ALPHA*min(u[i], u[j])-0.5*np.exp(-ALPHA*max(u[i], u[j]))*(np.exp(ALPHA*min(u[i], u[j]))-np.exp(-ALPHA*min(u[i], u[j]))))
                if i != j: W[j, i] = W[i, j]

        W_INV = np.linalg.inv(W)
        ZETA = W_INV@P_M

        X = np.sum(u*m*ZETA)
        Y = np.sum(S*m*ZETA)

        PP = np.exp(-ltfr*cp)*(1+ALPHA*X-np.exp(-ALPHA*cp)*Y)
        dPP = -ltfr*PP + np.exp(-ltfr*cp)*ALPHA*np.exp(-ALPHA*cp)*Y

        FWD = -1/PP*dPP

        if itr == 0:
            PP = np.exp(-ltfr*np.max(u))*(1+ALPHA*X-np.exp(-ALPHA*np.max(u))*Y)
            dPP = -ltfr*PP + np.exp(-ltfr*np.max(u))*ALPHA*np.exp(-ALPHA*np.max(u))*Y
            temp = -1/PP*dPP

            TARGET_FWD = np.log(np.exp(ltfr)+tol) if temp > ltfr else np.log(np.exp(ltfr)-tol)

        if TARGET_FWD < ltfr:
            if FWD < TARGET_FWD: ALPHA_LB = ALPHA
            else: ALPHA_UB = ALPHA
        else:
            if FWD < TARGET_FWD: ALPHA_UB = ALPHA
            else: ALPHA_LB = ALPHA

    return 0.5*(ALPHA_UB+ALPHA_LB)


def Cont2Discrete(spot_cont: np.ndarray) -> np.ndarray:
    return np.exp(spot_cont)-1


def SmithWilson(ltfr: float, alpha: float, tenor: np.ndarray, spot_cont_input: np.ndarray, t_out) -> np.ndarray:
    '''부채 현물 금리 구하는 함수'''
    
    ltfr = np.log(1+ltfr)
    n = len(tenor)
    N_out = len(t_out)
    u = tenor.copy()
    P = np.exp(-spot_cont_input*u)
    m = np.exp(-ltfr*u)
    P_M = P-m

    W = np.zeros([n, n])
    for i in range(n):
        for j in range(n):
            W[i, j] = np.exp(-ltfr*(u[i]+u[j]))*(alpha*min(u[i], u[j])-0.5*np.exp(-alpha*max(u[i], u[j]))*(np.exp(alpha*min(u[i], u[j]))-np.exp(-alpha*min(u[i], u[j]))))
            if i != j: W[j, i] = W[i, j]

    W_INV = np.linalg.inv(W)
    ZETA = W_INV@P_M

    t = np.fmax(t_out, 1e-6)
    W2 = np.zeros([N_out, n])
    for i in range(N_out):
        for j in range(n):
            W2[i, j] = np.exp(-ltfr * (t[i] + u[j])) * (alpha * min(t[i], u[j]) - 0.5 * np.exp(-alpha * max(t[i], u[j])) * (np.exp(alpha * min(t[i], u[j])) - np.exp(-alpha * min(t[i], u[j]))))

    return -np.log(W2@ZETA+np.exp(-ltfr*t))/t


def YTMPrice(tenor: float, ytm: float, freq: int) -> float:
    '''YTM을 이용한 채권가격을 구하는 함수'''
    
    if freq == 0:
        return 1/(1+ytm)**tenor

    dt = 1/freq
    P = 0
    t = tenor.copy()
    while t > 0:
        if t==tenor:
            cf = 1 + ytm/freq
        else:
            cf = ytm/freq
        
        if abs(t/dt-int(t/dt)) < 1e-7:
            df = (1+ytm/freq)**(-t*freq)
        else:
            df = 1/(1+ytm*t)
        
        P += cf*df
        t -= dt
    return P


def SmithWilsonYTM(ltfr: float, alpha: float, tenor: np.ndarray, ytm: np.ndarray, freq: int, t_out: np.ndarray) -> np.ndarray:
    '''자산 현물 금리 구하는 함수'''

    ltfr = np.log(1+ltfr)
    n = len(tenor)
    N_out = len(t_out)
    if freq != 0:
        k = int(sum(np.ceil(tenor*freq)))
        C_col_candidate = np.zeros(k)
        C_col_candidate2 = np.zeros(k)

        k = 0
        for i in range(n):
            for j in range(int(np.ceil(tenor[i]*freq))):
                C_col_candidate[k] = tenor[i] - j*1/freq
                k += 1

        N2 = 0
        for i in range(len(C_col_candidate)):
            tmp = np.min(C_col_candidate)
            if tmp == 99999: break
            C_col_candidate2[N2] = tmp
            N2 += 1
            for j in range(len(C_col_candidate)):
                if C_col_candidate[j] == tmp: C_col_candidate[j] = 99999

        t = np.zeros(N2)
        for i in range(N2):
            t[i] = C_col_candidate2[i]

        c = np.zeros([n, N2])
        for i in range(n):
            tmp = tenor[i]
            for j in range(N2):
                if t[j] > tmp:
                    c[i, j] = 0
                elif tmp == t[j]:
                    c[i, j] = 1 + ytm[i]/freq
                elif int((tmp - t[j])*12) % int(12/freq) == 0:
                    c[i, j] = ytm[i]/freq
                else:
                    c[i, j] = 0
    else:
        N2 = n
        t = tenor.copy()
        c = np.identity(n)

    m = np.zeros(n)
    for i in range(n):
        m[i] = YTMPrice(tenor[i], ytm[i], freq)
    u = np.exp(-ltfr*t)

    W = np.zeros([N2, N2])
    for i in range(N2):
        for j in range(i, N2):
            W[i, j] = np.exp(-ltfr * (t[i] + t[j])) * (alpha * min(t[i], t[j]) - 0.5 * np.exp(-alpha * max(t[i], t[j])) * (np.exp(alpha * min(t[i], t[j])) - np.exp(-alpha * min(t[i], t[j]))))
            if i != j: W[j, i] = W[i, j]

    m_Cu = m - c@u
    ZETA = np.linalg.inv(c@W@c.T)@m_Cu
    ZETA2 = c.T@ZETA

    result = np.zeros(N_out)
    tt = np.fmax(t_out, 1e-6)
    for i in range(N_out):
        tmp = np.exp(-ltfr*tt[i])
        for j in range(N2):
            tmp += ZETA2[j] * (np.exp(-ltfr * (tt[i] + t[j])) * (alpha * min(tt[i], t[j]) - 0.5 * np.exp(-alpha * max(tt[i], t[j])) * (np.exp(alpha * min(tt[i], t[j])) - np.exp(-alpha * min(tt[i], t[j])))))
        result[i] = -np.log(tmp) / tt[i]
        
    return result


if __name__ == '__main__':
    t = np.arange(1202)
    t_out = t/12

    # Inputs
    alpha0 = 0.1
    ltfr = 0.052
    freq = 2
    spread = 0.00481
    cp = 60
    tol = 1e-4
    llp = 20
    tenor0 = np.array([0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4, 5, 7, 10, 15, 20, 30, 50])
    ytm = np.array([0.00416, 0.00527, 0.00595, 0.00656, 0.008, 0.00886, 0.00974, 0.0097, 0.01168, 0.01335, 0.01528, 0.01722, 0.01802, 0.01832, 0.01832, 0.01827])
    shock_cont = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

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

    # Unit Test
    assert np.allclose(SmithWilson_ALPHA(ltfr, tenor, spot_cont_input, cp, tol), 0.131812241249148)
    assert np.allclose(sum(Cont2Discrete(SmithWilson(ltfr, alpha, tenor, spot_cont_input, t_out))**2), 1.51253390533584)
    assert np.allclose(sum(Cont2Discrete(SmithWilsonYTM(ytm[tenor0.argmax()], alpha0, tenor0, ytm, freq, t_out))**2), 0.387538672437389)