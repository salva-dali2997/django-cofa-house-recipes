
function RecipeCard({recipe_id, recipe_name}) {
  return (
    <li>
      <a 
      href={`/recipes/${recipe_id}`}
      className="px-4 py-8 rounded-xl text-rust-dark2 text-outline
      hover:text-cream text-center transition-colors 
        shadow-lg block w-full text-2xl font-bold
        bg-radial-[at_50%_75%] from-dark-salmon from-85% to-peach
        active:scale-95 border border-gray-50">
      {recipe_name}</a>
    </li>
  )
}

export default RecipeCard;