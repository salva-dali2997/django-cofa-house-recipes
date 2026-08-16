import RecipeList from './RecipeList.jsx';
import RecipeCreate from './RecipeCreate.jsx';

function App({ recipes }) {
  return <RecipeList recipes={recipes} />;
}

export default App;
