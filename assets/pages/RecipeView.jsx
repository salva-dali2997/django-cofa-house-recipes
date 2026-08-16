// ingredients: Array<{ quantity: string, ingredient__name: string }>
// TODO: refactor to reuse RecipeCard (or a similar shared list-item component) instead of inline <li> markup
function RecipeView({ recipe, ingredients }) {
  return (
    <div className="max-w-150 mx-auto text-center">
      <h1 className="text-3xl text-rust font-bold mb-2">{recipe.name}</h1>
      <ul className="list-none bg-peach p-4">
        {ingredients.map((ingredient, index) => (
          <li key={index} className="flex justify-between text-center text-xl px-10 py-4">
            <span>{ingredient.ingredient__name}</span>
            <span>{ingredient.quantity}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RecipeView;