import { createRoot } from 'react-dom/client';
import Signup from '../pages/Signup';

let context = {
  "csrf_token": JSON.parse(document.getElementById('csrf_token').textContent),
  "username": JSON.parse(document.getElementById('username').textContent),
  "password1": JSON.parse(document.getElementById('password1').textContent),
  "password2": JSON.parse(document.getElementById('password2').textContent),
  "code": JSON.parse(document.getElementById('code').textContent),
  "error": JSON.parse(document.getElementById('error').textContent),
}

createRoot(document.getElementById('root')).render(<Signup context={context} />);