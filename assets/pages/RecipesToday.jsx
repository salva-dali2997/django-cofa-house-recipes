import RecipeCard from '../components/RecipeCard.jsx';
import RisoFood from '../components/RisoFood.jsx';

function RecipesToday({ context }) {
  const recipes = context["recipes_data"];

  return (
    <div className="px-4 sm:px-6 lg:px-10 pb-10 text-center">
      <header className="flex items-center justify-center gap-4 sm:gap-6 mb-8">
        <RisoFood food="grapefruit" className="hidden sm:block w-16 -rotate-12" />
        <h1 className="font-display text-3xl sm:text-4xl text-rust-dark title-squiggle">Today’s Recipes</h1>
        <RisoFood food="mushroom" className="hidden sm:block w-16 rotate-6" />
      </header>
      {recipes.length === 0 ? (
        <div className="flex flex-col items-center py-6">
          <RisoFood food="mushroom" className="w-28 mb-2" />
          <p className="text-rust-dark/70">Nothing’s on the menu yet — check back soon.</p>
        </div>
      ) : (
        <ul className="list-none grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 max-w-5xl mx-auto">
          {recipes.map((recipe) => (
            <RecipeCard key={recipe.id} recipe_id={recipe.id} recipe_name={recipe.name}></RecipeCard>
          ))}
        </ul>
      )}
    </div>
  );
}

export default RecipesToday;
