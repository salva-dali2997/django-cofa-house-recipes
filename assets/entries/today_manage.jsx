import { createRoot } from 'react-dom/client';
import MenuManage from '../pages/MenuManage.jsx';

let context = {
  "recipes_data": JSON.parse(document.getElementById('recipes_data').textContent),
  "csrf_token": JSON.parse(document.getElementById('csrf_token').textContent),
}

createRoot(document.getElementById('root')).render(<MenuManage context={context} />);
