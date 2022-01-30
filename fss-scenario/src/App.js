import { Routes, Route } from 'react-router-dom';
import Simulation from './Simulation';
import Menu from './Menu';

function App() {
  return (
    <div>
      <Menu />

      <Routes>
        <Route path="/simulation" element={ <Simulation /> } />
        <Route path="/" />
      </Routes>
    </div>
  )
}

export default App;