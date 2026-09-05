import { createRoot } from 'react-dom/client';
import RecipeCreate from '../pages/RecipeCreate.jsx';

let context = {
  "csrf_token": JSON.parse(document.getElementById('csrf_token').textContent),
  "recipe": JSON.parse(document.getElementById('recipe').textContent),
  "ingredients": JSON.parse(document.getElementById('ingredients').textContent),
  "suggestions": JSON.parse(document.getElementById('suggestions').textContent),
}

createRoot(document.getElementById('root')).render(<RecipeCreate context={context} />);