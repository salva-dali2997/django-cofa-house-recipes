import { createRoot } from 'react-dom/client';
import RecipeCreate from './RecipeCreate.jsx';

let context = {
  "csrf_token": JSON.parse(document.getElementById('csrf-token').textContent),
  "recipe": JSON.parse(document.getElementById('recipe').textContent),
  "ingredients": JSON.parse(document.getElementById('ingredients').textContent),
}

createRoot(document.getElementById('root')).render(<RecipeCreate context={context} />);