import { useState } from 'react';

function MenuManage({ context }) {
  const [recipes, setRecipes] = useState(context["recipes_data"]);

  async function toggleRecipe(recipeId) {
    const formData = new FormData();
    formData.append("csrfmiddlewaretoken", context["csrf_token"]);
    formData.append("recipe_id", recipeId);
    const response = await fetch("/recipes/today/toggle", {
      method: "POST",
      body: formData,
    });
    if (!response.ok) return;
    const updated = await response.json();
    setRecipes((prev) =>
      prev.map((recipe) =>
        recipe.id === updated.id ? { ...recipe, on_menu: updated.on_menu } : recipe
      )
    );
  }

  return (
    <div className="px-4 sm:px-6 lg:px-10 pb-10 text-center">
      <h1 className="font-display text-3xl sm:text-4xl text-rust-dark title-squiggle mb-8">Manage Today's Menu</h1>
      <ul className="list-none max-w-xl mx-auto text-left rounded-2xl bg-dark-salmon/40 divide-y divide-rust-dark/15 overflow-hidden">
        {recipes.map((recipe) => (
          <li key={recipe.id} className="flex items-center justify-between gap-4 px-4 sm:px-6 py-1">
            <span className="text-rust-dark text-base sm:text-lg">{recipe.name}</span>
            <label className="flex items-center justify-center w-11 h-11 shrink-0 cursor-pointer">
              <input
                type="checkbox"
                className="riso-checkbox"
                checked={recipe.on_menu}
                onChange={() => toggleRecipe(recipe.id)}
              />
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MenuManage;
