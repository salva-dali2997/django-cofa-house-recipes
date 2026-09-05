import { createRoot } from 'react-dom/client';
import NavBar from '../components/NavBar.jsx';

let context = {
  "user_authenticated": JSON.parse(document.getElementById('user_authenticated').textContent),
}

createRoot(document.getElementById('navbar-root')).render(<NavBar context={context}/>);