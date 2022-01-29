import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import './App.css';

function App() {

  const [currency, setCurrency] = useState('KRW');
  const [baseDate, setBaseDate] = useState('20211231');
  const [isCustomSetting, setIsCustomSetting] = useState(false);
  const [data, setData] = useState('');
  const [ltfr, setLtfr] = useState(0.0495);
  const [spread, setSpread] = useState(0.00495);
  const [llp, setLlp] = useState(20);
  const [cp, setCp] = useState(60);
  const [freq, setFreq] = useState(2);
  const [tenor, setTenor] = useState('0.25,0.5,0.75,1,1.5,2,2.5,3,4,5,7,10,15,20,30,50');
  const [shockCont, setShockCont] = useState('0,0,0,0,0,0,0,0,0,0,0,0,0,0');

  const calculate = () => {
    const params = {
      custom_setting: isCustomSetting,
      currency: currency,
      base_date: baseDate
    }
    axios.get('http://127.0.0.1:8000', {params})
      .then(res => setData(res.data));
  }

  const download = () => {
    const blob = new Blob([JSON.stringify(data)], {type: "application/json"});
    const fileDownloadUrl = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = fileDownloadUrl;
    a.download = 'test.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
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
      <Plot data={[{
          x: data.t,
          y: data.forward_disc_liab,
          type: 'scatter',
          mode: 'lines',
          name: 'Liability',
          marker: {color: '#009473'},
          hovertemplate: 'Tenor: %{x}M<br>Rate: %{y:,.3%}'
        }, {
          x: data.t,
          y: data.forward_disc_asset,
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
          </table>
          <div className="btnDiv">
            <button className="btn" id="btn_calc" onClick={calculate}>계산</button>
            <button className="btn" id="btn_download" onClick={download}>다운</button>
          </div>
        </div>
        {/* 오른쪽 */}
        <table>
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
            <input type="checkbox" value={isCustomSetting} onChange={onCustomSettingCheckHandler} /> 자동설정
          </tr>
        </table>
      </div>
      
  
      
    </>
  );
}

export default App;
