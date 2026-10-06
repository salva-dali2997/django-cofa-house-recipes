import RecipeList from './RecipeList.jsx';

function App({ recipes, pagination }) {
  return <RecipeList recipes={recipes} pagination={pagination} />;
}

export default App;
