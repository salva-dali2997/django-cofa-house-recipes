import { useState } from 'react';
import Button from '../components/Button.jsx'

function RecipeCreate({ context }) {
  const suggestions_object = Object.fromEntries(context.suggestions);
  const [ingredients, setIngredients] = useState(context.ingredients);
  const [confirm_create, setConfirm] = useState(ingredients.map(() => false));
  const addIngredient = () => {
    setIngredients([...ingredients, {name: "", quantity: ""}]);
    setConfirm([...confirm_create, false]);
  };
  const updateIngredientName = (indexToUpdate, ingredientName) => {
    setIngredients(ingredients => 
      ingredients.map((ingredient, index) => 
        index === indexToUpdate ? {...ingredient, name : ingredientName} : {...ingredient}));
  }
  const acceptSuggestion = (indexToUpdate, suggestedName) => {
    setConfirm(confirm_create => confirm_create.with(indexToUpdate, true));
    updateIngredientName(indexToUpdate, suggestedName);
  }
  const denySuggestion = (indexToUpdate) => {
    setConfirm(confirm_create => confirm_create.with(indexToUpdate, true));
  }
  return (
    <div className="text-rust ml-10">
      <h1 className="text-3xl font-bold mb-2">Create a Recipe</h1>
      <form action="/recipes/create" method="post">
      <input type="hidden" name="csrfmiddlewaretoken" value={context["csrf_token"]}></input>
        <div className="mb-5 text-xl">
          <label htmlFor="name">Recipe Name: </label>
          <input type="text" id="name" name="name" placeholder="Recipe" defaultValue={context.recipe.name} required />
        </div>
        {ingredients.map((ingredient, index) => {
          const suggestion = suggestions_object[index];
          return (
            <div key={index} className="space-y-3 text-xl">
              <label htmlFor="ingredient">Ingredient Name: </label>
              <input type="text" id={`ingredient-${index}`} 
                name={`ingredients-${index}-name`} 
                placeholder="Ingredient" value={ingredient.name} 
                onChange={(event) => {
                  updateIngredientName(index, event.target.value); 
                  setConfirm(confirm_create => confirm_create.with(index, false));
                }}/>
              <label htmlFor="quantity">Quantity: </label>
              <input type="text" id={`quantity-${index}`} name={`ingredients-${index}-quantity`} placeholder="Quantity" defaultValue={ingredient.quantity}/>
              {suggestion && !confirm_create[index] ? 
                <div className="flex gap-x-2">
                  did you mean {suggestion}? you entered {ingredient.name}
                  <Button className="text-black" onClick={() => acceptSuggestion(index, suggestion)}>Confirm suggestion</Button>
                  <Button className="text-black" onClick={() => denySuggestion(index, suggestion)}>Deny suggestion</Button>
                </div>
              :null}
              <input type="hidden" name={`ingredients-${index}-confirmed`} value={confirm_create[index] ? true : ""} readOnly/>
            </div>
          )
        }
        )}
        <div>
          <Button className="text-black" onClick={addIngredient} children="Add Ingredient"></Button>
        </div>
        <input type="hidden" name="ingredients-TOTAL_FORMS" value={ingredients.length} />
        <input type="hidden" name="ingredients-INITIAL_FORMS" value="0" />
        <input type="hidden" name="ingredients-MIN_NUM_FORMS" value="0" />
        <input type="hidden" name="ingredients-MAX_NUM_FORMS" value="1000" />
        <div className="mt-8">
          <Button type="submit" className="text-black" children="Create Recipe"></Button>
        </div>
      </form>
    </div>
  );
}

export default RecipeCreate;