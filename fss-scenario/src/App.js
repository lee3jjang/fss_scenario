import { Routes, Route } from 'react-router-dom';
import Simulation from './Simulation';
import Menu from './Menu';
import ReadMe from './ReadMe';
import DataImport from './DataImport';

function App() {
  return (
    <div>
      <Menu />

      <Routes>
        <Route path="/simulation" element={ <Simulation /> } />
        <Route path="/readme" element={ <ReadMe /> } />
        <Route path="/dataimport" element={ <DataImport /> } />
      </Routes>
    </div>
  )
}

export default App;