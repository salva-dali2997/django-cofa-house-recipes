import { useState } from 'react';

function RecipeCreate({ context }) {
  const [ingredients, setIngredients] = useState(context.ingredients);
  const addIngredient = () => {
    setIngredients([...ingredients, {name: "", quantity: ""}]);
  };
  return (
    <div>
      <h1>Create a Recipe</h1>
      <form action="/recipes/create" method="post">
      <input type="hidden" name="csrfmiddlewaretoken" value={context["csrf_token"]}></input>
        <div>
          <label htmlFor="name">Recipe Name:</label>
          <input type="text" id="name" name="name" placeholder="Recipe" defaultValue={context.recipe.name} required />
        </div>
        {ingredients.map((ingredient, index) =>
          <div key={index}>
            <label htmlFor="ingredient">Ingredient Name:</label>
            <input type="text" id={`ingredient-${index}`} name={`ingredients-${index}-name`} placeholder="Ingredient" defaultValue={ingredient.name}/>
            <input type="text" id={`quantity-${index}`} name={`ingredients-${index}-quantity`} placeholder="Quantity" defaultValue={ingredient.quantity}/>
          </div>
        )}
        <div>
          <button type="button" onClick={addIngredient}>Add Ingredient</button>
        </div>
        <input type="hidden" name="ingredients-TOTAL_FORMS" value={ingredients.length} />
        <input type="hidden" name="ingredients-INITIAL_FORMS" value="0" />
        <input type="hidden" name="ingredients-MIN_NUM_FORMS" value="0" />
        <input type="hidden" name="ingredients-MAX_NUM_FORMS" value="1000" />
        <div>
          <button type="submit">Create Recipe</button>
        </div>
      </form>
    </div>
  );
}

export default RecipeCreate;