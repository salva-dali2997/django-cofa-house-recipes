import RecipeCard from '../components/RecipeCard.jsx';

function RecipeList({ recipes, pagination }) {
  return (
    <div className="mx-5 text-center">
      <h1 className="text-4xl text-rust-dark font-bold mb-7 text-outline">All Recipes List</h1>
      <ul className="list-none grid lg:grid-cols-3 md:grid-cols-2 grid-cols-1 gap-10">
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
