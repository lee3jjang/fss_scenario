import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import './App.css';

function App() {

  const [currency, setCurrency] = useState('KRW');
  const [baseDate, setBaseDate] = useState('20211231');
  const [isCustomSetting, setIsCustomSetting] = useState(false);
  const [data, setData] = useState('');

  function fn() {
    const params = {
      custom_setting: isCustomSetting,
      currency: currency,
      base_date: baseDate
    }
    axios.get('http://127.0.0.1:8000', {params})
      .then(res => setData(res.data));
  }

  let download = () => {
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

  return (
    <>
      <Plot data={[{
          x: data.t,
          y: data.forward_disc_liab,
          type: 'scatter',
          mode: 'lines+markers',
          marker: {color: 'red'}
        }, {
          x: data.t,
          y: data.forward_disc_asset,
          type: 'scatter',
          mode: 'lines+markers',
          marker: {color: 'blue'}
        }]}
        layout={ {width: 640, height: 540, title: 'A Fancey Plot'} }
      />
      <input type="text" name="basedate"
        value={baseDate} minLength="8" maxLength="8"
        onChange={onBaseDateChangeHandler}
        required />
      <select id="currency-select"
        name="currency"
        value={currency}
        onChange={onCurrencyChangeHandler}>
        <option value="KRW">KRW</option>
        <option value="USD">USD</option>
        <option value="JPY">JPY</option>
      </select>
      <button className="btn" onClick={fn}>Get Data</button>
      <button className="btn" onClick={download}>Download</button>
    </>
  );
}

export default App;
