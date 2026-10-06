import { createRoot } from 'react-dom/client';
import RecipesToday from '../pages/RecipesToday.jsx';

let context = {
  "recipes_data": JSON.parse(document.getElementById('recipes_data').textContent),
}

createRoot(document.getElementById('root')).render(<RecipesToday context={context} />);
