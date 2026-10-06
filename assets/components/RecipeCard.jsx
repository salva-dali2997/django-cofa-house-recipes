import RisoFood, { foodForId } from './RisoFood.jsx';

function RecipeCard({recipe_id, recipe_name}) {
  return (
    <li>
      <a
        href={`/recipes/${recipe_id}`}
        className="group relative overflow-hidden flex items-center justify-center min-h-24 px-12 py-6 rounded-2xl
          bg-cream border-2 border-rust-dark/40 shadow-sm
          text-rust-dark hover:border-rust hover:text-rust hover:shadow-md
          active:scale-95 transition-all
          text-center text-xl sm:text-2xl font-bold font-display">
        <RisoFood
          food={foodForId(recipe_id)}
          className="absolute -right-3 -bottom-3 w-16 rotate-12 opacity-80
            group-hover:rotate-0 group-hover:opacity-100 transition-transform"
        />
        <span className="relative">{recipe_name}</span>
      </a>
    </li>
  )
}

export default RecipeCard;
