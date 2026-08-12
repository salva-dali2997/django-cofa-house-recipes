function RecipeList({ recipes }) {
  return (
    <ul className="list-none">
      {recipes.map((recipe) => (
        <li key={recipe.id}><a href={`/recipes/${recipe.id}`} className="hover:font-bold">{recipe.name}</a></li>
      ))}
    </ul>
  );
}

export default RecipeList;
