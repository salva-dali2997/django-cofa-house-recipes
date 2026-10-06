import { createRoot } from 'react-dom/client';
import NavBar from '../components/NavBar.jsx';

let context = {
  "user_authenticated": JSON.parse(document.getElementById('user_authenticated').textContent),
  "user_is_superuser": JSON.parse(document.getElementById('user_is_superuser').textContent),
}

createRoot(document.getElementById('navbar-root')).render(<NavBar context={context}/>);