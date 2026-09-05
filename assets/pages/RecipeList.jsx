import RecipeCard from '../components/RecipeCard.jsx';

function RecipeList({ recipes }) {
  return (
    <div className="mx-5 text-center">
      <h1 className="text-4xl text-rust-dark font-bold mb-7 text-outline">All Recipes List</h1>
      <ul className="list-none grid lg:grid-cols-3 md:grid-cols-2 grid-cols-1 gap-10">
        {recipes.map((recipe) => (
          <RecipeCard key={recipe.id} recipe_id={recipe.id} recipe_name={recipe.name}></RecipeCard>
        ))}
      </ul>
    </div>
  );
}

export default RecipeList;
