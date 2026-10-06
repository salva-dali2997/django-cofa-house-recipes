import RecipeCard from '../components/RecipeCard.jsx';
import Button from '../components/Button.jsx';
import RisoFood from '../components/RisoFood.jsx';

function RecipeList({ recipes, pagination }) {
  return (
    <div className="px-4 sm:px-6 lg:px-10 pb-10 text-center">
      <header className="flex items-center justify-center gap-4 sm:gap-6 mb-8">
        <RisoFood food="tomato" className="hidden sm:block w-16 -rotate-12" />
        <h1 className="font-display text-3xl sm:text-4xl text-rust-dark title-squiggle">All Recipes</h1>
        <RisoFood food="chili" className="hidden sm:block w-16 rotate-12" />
      </header>
      <ul className="list-none grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 max-w-5xl mx-auto">
        {recipes.map((recipe) => (
          <RecipeCard key={recipe.id} recipe_id={recipe.id} recipe_name={recipe.name}></RecipeCard>
        ))}
      </ul>
      {pagination.total_pages > 1 ? (
        <div className="flex items-center justify-center gap-3 sm:gap-4 mt-8">
          {pagination.has_previous ? (
            <Button href={`/recipes/?page=${pagination.previous_page}`}>← Previous</Button>
          ) : null}
          <span className="font-display text-lg sm:text-xl text-rust-dark">Page {pagination.current_page} of {pagination.total_pages}</span>
          {pagination.has_next ? (
            <Button href={`/recipes/?page=${pagination.next_page}`}>Next →</Button>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}

export default RecipeList;
