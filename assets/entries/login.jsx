import { createRoot } from 'react-dom/client';
import Login from '../pages/Login';

let context = {
  "csrf_token": JSON.parse(document.getElementById('csrf-token').textContent),
  "username": JSON.parse(document.getElementById('username').textContent),
  "password": JSON.parse(document.getElementById('password').textContent),
}

createRoot(document.getElementById('root')).render(<Login context={context} />);