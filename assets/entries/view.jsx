import { createRoot } from 'react-dom/client';
import RecipeView from '../pages/RecipeView.jsx';

let context = {
  "csrf_token": JSON.parse(document.getElementById('csrf_token').textContent),
  "recipe": JSON.parse(document.getElementById('recipe').textContent),
  "ingredients": JSON.parse(document.getElementById('ingredients').textContent),
  "comments": JSON.parse(document.getElementById('comments').textContent)
}

createRoot(document.getElementById('root')).render(<RecipeView context={context}/>);