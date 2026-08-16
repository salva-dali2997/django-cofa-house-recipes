import { createRoot } from 'react-dom/client';
import RecipeView from '../pages/RecipeView.jsx';

const recipe = JSON.parse(document.getElementById('recipe').textContent);
const ingredients = JSON.parse(document.getElementById('ingredients').textContent);

createRoot(document.getElementById('root')).render(<RecipeView recipe={recipe} ingredients={ingredients}/>);