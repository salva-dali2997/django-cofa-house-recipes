import RecipeCard from '../components/RecipeCard.jsx';

function RecipeList({ recipes }) {
  return (
    <div className="mx-5 text-center">
      <h1 className="text-3xl text-rust font-bold mb-2">All Recipes List</h1>
      <ul className="list-none grid grid-cols-3 gap-10">
        {recipes.map((recipe) => (
          <RecipeCard key={recipe.id} recipe_id={recipe.id} recipe_name={recipe.name}></RecipeCard>
        ))}
      </ul>
    </div>
  );
}

export default RecipeList;
