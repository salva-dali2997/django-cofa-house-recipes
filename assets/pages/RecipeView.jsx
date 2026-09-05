import { useState } from "react";
import Button from "../components/Button";
import Input from "../components/Input";

// ingredients: Array<{ quantity: string, ingredient__name: string }>
// TODO: refactor to reuse RecipeCard (or a similar shared list-item component) instead of inline <li> markup
function RecipeView({ context }) {
  const [comments, setComments] = useState(context["comments"]);

  async function handleCommentSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const response = await fetch("/recipes/comment", {
      method: "POST",
      body: new FormData(form),
    });
    if (!response.ok) return;
    const newComment = await response.json();
    setComments((prev) => [...prev, newComment]);
    form.reset();
  }

  return (
    <div className="max-w-150 mx-auto text-center">
      <h1 className="text-4xl text-rust-dark font-bold text-outline mb-2">{context["recipe"].name}</h1>
      <div>
        <ul className="list-none bg-dark-salmon p-4">
          {context["ingredients"].map((ingredient, index) => (
            <li key={`ingredient-${index}`} className="flex justify-between text-rust-dark text-outline text-center text-xl px-10 py-4">
              <span>{ingredient.ingredient__name}</span>
              <span>{ingredient.quantity}</span>
            </li>
          ))}
        </ul>
      </div>
      <div>
        <div className="bg-dark-salmon">
          <h2 className="text-2xl text-rust-dark text-outline font-bold mb-2 mt-8">Comments</h2>
          <ul className="list-none p-4">
            {comments.map((comment, index) => (
              <li key={`comment-${index}`} className="flex justify-between text-rust-dark text-outline text-center text-xl px-10 py-4">
                <span>{comment.content}</span>
              </li>
            ))}
          </ul>
        </div>
        <form onSubmit={handleCommentSubmit}>
          <input type="hidden" name="csrfmiddlewaretoken" value={context["csrf_token"]} readOnly />
          <input type="hidden" name="recipe_id" value={context["recipe"].id} readOnly />
          <div className="mb-5 text-xl text-rust-dark text-outline">
            <label htmlFor="comment">Comment here</label>
            <Input type="text" id="comment" name="comment" required />
          </div>
          <Button type="submit" className="text-rust-dark text-outline">Comment</Button>
        </form>
      </div>
    </div>
  );
}

export default RecipeView;