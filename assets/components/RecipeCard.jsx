
function RecipeCard({recipe_id, recipe_name}) {
  return (
    <li>
      <a 
      href={`/recipes/${recipe_id}`}
      className="bg-peach px-4 py-8 rounded-xl hover:bg-rust 
      hover:text-cream text-center transition-colors 
        shadow-md block w-full text-xl">
      {recipe_name}</a>
    </li>
  )
}

export default RecipeCard;