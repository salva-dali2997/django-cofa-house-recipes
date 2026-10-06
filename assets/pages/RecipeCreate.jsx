import { useState, useRef } from 'react';
import Button from '../components/Button.jsx'
import Input from '../components/Input.jsx'

function RecipeCreate({ context }) {
  const suggestions_object = Object.fromEntries(context.suggestions);
  const [ingredients, setIngredients] = useState(context.ingredients);
  const [confirm_create, setConfirm] = useState(ingredients.map(() => false));
  const [directions, setDirections] = useState(context.recipe.directions || "1. ");
  const directionsRef = useRef(null);
  const handleDirectionsKeyDown = (event) => {
    if (event.key !== "Enter") return;
    event.preventDefault();
    const textarea = directionsRef.current;
    const { selectionStart, selectionEnd, value } = textarea;
    const lineNumber = value.slice(0, selectionStart).split("\n").length;
    const insert = `\n${lineNumber + 1}. `;
    const newValue = value.slice(0, selectionStart) + insert + value.slice(selectionEnd);
    setDirections(newValue);
    requestAnimationFrame(() => {
      const cursorPosition = selectionStart + insert.length;
      textarea.setSelectionRange(cursorPosition, cursorPosition);
    });
  };
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
  const textareaClasses = "block w-full min-h-40 py-2 px-4 border-b-2 border-rust-dark/30 rounded-md focus:outline-none focus:ring-2 focus:ring-rust bg-cream text-base";
  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-10 py-8 lg:py-12">
      <h1 className="font-display text-3xl lg:text-4xl text-rust-dark mb-6 lg:mb-8">Create a Recipe</h1>
      <form action="/recipes/create" method="post" className="lg:grid lg:grid-cols-2 lg:gap-x-12 lg:gap-y-10">
        <input type="hidden" name="csrfmiddlewaretoken" value={context["csrf_token"]}></input>

        <div className="mb-6 lg:col-span-2 lg:mb-0">
          <label htmlFor="name" className="block text-rust-dark font-semibold mb-1">Recipe Name</label>
          <Input type="text" id="name" name="name" placeholder="Recipe" defaultValue={context.recipe.name} required className="w-full lg:max-w-md" />
        </div>

        <div className="mb-8 lg:mb-0">
          <label htmlFor="directions" className="block text-rust-dark font-semibold mb-1">Directions</label>
          <textarea
            ref={directionsRef}
            id="directions"
            name="directions"
            rows={10}
            className={textareaClasses}
            value={directions}
            onChange={(event) => setDirections(event.target.value)}
            onKeyDown={handleDirectionsKeyDown}
          />
        </div>

        <div>
          <h2 className="text-rust-dark font-semibold mb-1">Ingredients</h2>
          <div className="flex flex-col gap-3">
            {ingredients.map((ingredient, index) => {
              const suggestion = suggestions_object[index];
              return (
                <div key={index} className="rounded-xl border border-rust-dark/25 bg-dark-salmon/25 p-3 flex flex-col gap-2">
                  <div className="flex flex-col sm:flex-row gap-2">
                    <div className="flex-1">
                      <label htmlFor={`ingredient-${index}`} className="block text-sm text-rust-dark/80 mb-1">Ingredient</label>
                      <Input
                        type="text" id={`ingredient-${index}`}
                        name={`ingredients-${index}-name`}
                        placeholder="Ingredient" value={ingredient.name}
                        className="w-full"
                        onChange={(event) => {
                          updateIngredientName(index, event.target.value);
                          setConfirm(confirm_create => confirm_create.with(index, false));
                        }}/>
                    </div>
                    <div className="sm:w-32 shrink-0">
                      <label htmlFor={`quantity-${index}`} className="block text-sm text-rust-dark/80 mb-1">Quantity</label>
                      <Input type="text" id={`quantity-${index}`} name={`ingredients-${index}-quantity`} placeholder="Quantity" defaultValue={ingredient.quantity} className="w-full" />
                    </div>
                  </div>
                  {suggestion && !confirm_create[index] ?
                    <div className="rounded-lg bg-peach/40 border border-peach px-3 py-2 text-sm text-rust-dark flex flex-wrap items-center gap-2">
                      <span>Did you mean <strong>{suggestion}</strong>? You entered “{ingredient.name}”.</span>
                      <div className="flex flex-wrap gap-2 sm:ml-auto">
                        <Button className="text-sm" onClick={() => acceptSuggestion(index, suggestion)}>Use “{suggestion}”</Button>
                        <Button className="text-sm" onClick={() => denySuggestion(index, suggestion)}>Keep mine</Button>
                      </div>
                    </div>
                  : null}
                  <input type="hidden" name={`ingredients-${index}-confirmed`} value={confirm_create[index] ? true : ""} readOnly/>
                </div>
              )
            }
            )}
          </div>
          <Button className="mt-3" onClick={addIngredient}>+ Add Ingredient</Button>
          <input type="hidden" name="ingredients-TOTAL_FORMS" value={ingredients.length} />
          <input type="hidden" name="ingredients-INITIAL_FORMS" value="0" />
          <input type="hidden" name="ingredients-MIN_NUM_FORMS" value="0" />
          <input type="hidden" name="ingredients-MAX_NUM_FORMS" value="1000" />
        </div>

        <div className="mt-8 lg:col-span-2">
          <Button type="submit" className="w-full sm:w-auto">Create Recipe</Button>
        </div>
      </form>
    </div>
  );
}

export default RecipeCreate;
