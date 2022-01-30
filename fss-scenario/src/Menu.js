import './Menu.css';
import { Link } from 'react-router-dom';

function Menu() {
  return (
    <ul id="nav">
      <li><Link to="/simulation">시뮬레이션</Link></li>
      <li><Link to="/">데이터입력</Link></li>
      <li><Link to="/">배치작업</Link></li>
      <li><Link to="/">용어 및 사용법</Link></li>
    </ul>
  );
}

export default Menu;