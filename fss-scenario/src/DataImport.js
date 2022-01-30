import './DataImport.css';

function DataImport () {

  return (
    <table className="dataframe">
      <thead>
        <tr>
          <th>이름</th>
          <th>나이</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>이상진</td>
          <td>33</td>
        </tr>
        <tr>
          <td>이지원</td>
          <td>28</td>
        </tr>
      </tbody>
    </table>
  );
}

export default DataImport;