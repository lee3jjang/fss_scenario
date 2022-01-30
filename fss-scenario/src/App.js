import { Routes, Route } from 'react-router-dom';
import Simulation from './Simulation';
import Menu from './Menu';
import ReadMe from './ReadMe';

function App() {
  return (
    <div>
      <Menu />

      <Routes>
        <Route path="/simulation" element={ <Simulation /> } />
        <Route path="/readme" element={ <ReadMe /> } />
      </Routes>
    </div>
  )
}

export default App;