import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import './Simulation.css';
import Menu from './Menu';

function Simulation() {
  
  const [intRate, setIntRate] = useState({});
  const [info, setInfo] = useState({});
  const [baseDate, setBaseDate] = useState('20211231');
  const [currency, setCurrency] = useState('KRW');
  const [ltfr, setLtfr] = useState(0.0495);
  const [spread, setSpread] = useState(0.00495);
  const [llp, setLlp] = useState(20);
  const [cp, setCp] = useState(60);
  const [freq, setFreq] = useState(2);
  const [tenor, setTenor] = useState('0.25,0.5,0.75,1,1.5,2,2.5,3,4,5,7,10,15,20,30,50');
  const [shockCont, setShockCont] = useState('0,0,0,0,0,0,0,0,0,0,0,0,0,0');
  const [isCustomSetting, setIsCustomSetting] = useState(false);

  const calculate = () => {
    const params = {
      base_date: baseDate,
      currency: currency,
      ltfr: ltfr,
      spread: spread,
      llp: llp,
      cp: cp,
      freq: freq,
      tenor0: tenor,
      shock_cont: shockCont
    }

    axios.get('http://127.0.0.1:8000', {params})
      .then(res => {
        setIntRate(res.data.data);
        setInfo(res.data.info);
      })

    const now = new Date(Date.now());
    document.getElementById('log').textContent += `[${now.getFullYear()}.${now.getMonth()+1}.${now.getDate()} ${now.getHours()}:${now.getMinutes()}:${now.getSeconds()}] 계산 정보\n`
      + `baseDate=${info.baseDate}, currency=${info.currency}, ltfr=${info.ltfr}, spread=${info.spread}, llp=${info.llp}, cp=${info.cp}, freq=${info.freq},\ntenor=${info.tenor}\nytm=${info.ytm}\nshockCont=${info.shockCont}\n`;
  }

  const download = () => {
    let intRateCsv = [["t", "forwardDiscAsset", "forwardDiscLiab", "spotDiscAsset", "spotDiscLiab"]];
    let intRateTemp = [];
    for (let i=0; i<intRate.t.length; i++) {
      intRateTemp = [];
      intRateTemp.push(intRate.t[i]);
      intRateTemp.push(intRate.forwardDiscAsset[i]);
      intRateTemp.push(intRate.forwardDiscLiab[i]);
      intRateTemp.push(intRate.spotDiscAsset[i]);
      intRateTemp.push(intRate.spotDiscLiab[i]);
      intRateCsv.push(intRateTemp.join(","));
    }
    const resultCsv = intRateCsv.join("\n");
    
    const blob = new Blob([resultCsv], {type: "text/csv"});
    const fileDownloadUrl = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = fileDownloadUrl;
    a.download = 'int_rate.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);



    const now = new Date(Date.now());
    document.getElementById('log').textContent += `[${now.getFullYear()}.${now.getMonth()+1}.${now.getDate()} ${now.getHours()}:${now.getMinutes()}:${now.getSeconds()}] ` + '다운로드 실행\n';
  }

  const onCurrencyChangeHandler = (e) => {
    setCurrency(e.target.value);
  }
  const onBaseDateChangeHandler = (e) => {
    setBaseDate(e.target.value);
  }
  const onCustomSettingCheckHandler = (e) => {
    setIsCustomSetting(!isCustomSetting);
  }
  const onLtfrChangeHandler = (e) => {
    setLtfr(e.target.value);
  }
  const onSpreadChangeHandler = (e) => {
    setSpread(e.target.value);
  }
  const onCpChangeHandler = (e) => {
    setCp(e.target.value);
  }
  const onLlpChangeHandler = (e) => {
    setLlp(e.target.value);
  }
  const onFreqChangeHandler = (e) => {
    setFreq(e.target.value);
  }
  const onTenorChangeHandler = (e) => {
    setTenor(e.target.value);
  }
  const onShockContChangeHandler = (e) => {
    setShockCont(e.target.value);
  }

  return (
    <>
      <Menu />
      <Plot data={[{
          x: intRate.t,
          y: intRate.forwardDiscLiab,
          type: 'scatter',
          mode: 'lines',
          name: 'Liability',
          marker: {color: '#009473'},
          hovertemplate: 'Tenor: %{x}M<br>Rate: %{y:,.3%}'
        }, {
          x: intRate.t,
          y: intRate.forwardDiscAsset,
          type: 'scatter',
          mode: 'lines',
          name: 'Asset',
          marker: {color: '#dd4124'},
          hovertemplate: 'Tenor: %{x}M<br>Rate: %{y:,.3%}'
        }]}
        layout={{
          font: {
            family: 'Noto Sans KR, serif',
            size: 13,
            color: '#323232'
          },
          width: 840,
          height: 450,
          title: '1M Forward Rate',
          xaxis: {
            showgrid: false,
            zeroline: false,
            showline: true,
            title: 'Tenor (Month)',
            linecolor: '#323232',
            linewidth: 1
          },
          yaxis: {
            showgrid: false,
            zeroline: false,
            showline: true,
            title: 'Forward Rate (%)',
            tickformat: ',.1%',
            linecolor: '#323232',
            linewidth: 1
          },
          paper_bgcolor: '#fbfbfb',
          plot_bgcolor: '#fbfbfb'
        }}
      />

      <div className="setting">
        {/* 왼쪽 */}
        <div>
          <table>
            <tbody>
              <tr>
                <td>기준일자</td>
                <td><input type="text" value={baseDate} onChange={onBaseDateChangeHandler} required /></td>
              </tr>
              <tr>
                <td>화폐</td>
                <td>
                  <select value={currency} onChange={onCurrencyChangeHandler}>
                    <option value="KRW">KRW</option>
                    <option value="USD">USD</option>
                    <option value="JPY">JPY</option>
                  </select>
                </td>
              </tr>
            </tbody>
          </table>
          <div className="btnDiv">
            <button className="btn" id="btnCalc" onClick={calculate}>계산</button>
            <button className="btn" id="btnDownload" onClick={download}>다운</button>
          </div>
        </div>
        {/* 오른쪽 */}
        <table>
          <tbody>
            <tr>
              <td>LTFR</td>
              <td><input type="text" value={ltfr} onChange={onLtfrChangeHandler} required /></td>
            </tr>
            <tr>
              <td>스프레드</td>
              <td><input type="text" value={spread} onChange={onSpreadChangeHandler} required /></td>
            </tr>
            <tr>
              <td>최종관찰만기</td>
              <td><input type="text" value={llp} onChange={onLlpChangeHandler} required /></td>
            </tr>
            <tr>
              <td>수렴시점</td>
              <td><input type="text" value={cp} onChange={onCpChangeHandler} required /></td>
            </tr>
            <tr>
              <td>이자지급주기</td>
              <td><input type="text" value={freq} onChange={onFreqChangeHandler} required /></td>
            </tr>
            <tr>
              <td>테너</td>
              <td><input type="text" value={tenor} onChange={onTenorChangeHandler} required /></td>
            </tr>
            <tr>
              <td>충격시나리오</td>
              <td><input type="text" value={shockCont} onChange={onShockContChangeHandler} required /></td>
            </tr>
            <tr>
              <td>
                <input type="checkbox" value={isCustomSetting} onChange={onCustomSettingCheckHandler} /> 자동설정
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <textarea id="log" rows="10" cols="105" readOnly />
    </>
  );
}

export default Simulation;
