import { useState } from "react";
import Button from "../components/Button";
import Input from "../components/Input";
import RisoFood, { foodForId } from "../components/RisoFood";

const RELATIVE_TIME_UNITS = [
  ["year", 60 * 60 * 24 * 365],
  ["month", 60 * 60 * 24 * 30],
  ["week", 60 * 60 * 24 * 7],
  ["day", 60 * 60 * 24],
  ["hour", 60 * 60],
  ["minute", 60],
];
const relativeTimeFormatter = new Intl.RelativeTimeFormat("en", { numeric: "auto" });

// isoString: string produced by Django's DateTimeField/json_script (UTC ISO 8601)
function timeAgo(isoString) {
  const diffSeconds = (new Date(isoString) - new Date()) / 1000;
  for (const [unit, secondsInUnit] of RELATIVE_TIME_UNITS) {
    if (Math.abs(diffSeconds) >= secondsInUnit) {
      return relativeTimeFormatter.format(Math.round(diffSeconds / secondsInUnit), unit);
    }
  }
  return relativeTimeFormatter.format(Math.round(diffSeconds), "second");
}

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
    <div className="max-w-2xl mx-auto px-4 sm:px-6 pb-16">
      <header className="flex flex-col items-center mb-8">
        <RisoFood food={foodForId(context["recipe"].id)} className="w-20 sm:w-24 -rotate-6 mb-1" />
        <h1 className="font-display text-3xl sm:text-4xl text-rust-dark text-center title-squiggle">{context["recipe"].name}</h1>
      </header>

      <section>
        <h2 className="font-display text-xl sm:text-2xl text-rust-dark mb-3">Ingredients</h2>
        <div aria-hidden="true" className="h-4 rounded-t-2xl bg-gingham" />
        <ul className="list-none rounded-b-2xl bg-dark-salmon/40 divide-y divide-rust-dark/15 overflow-hidden">
          {context["ingredients"].map((ingredient, index) => (
            <li key={`ingredient-${index}`} className="flex items-center justify-between gap-4 px-4 sm:px-6 py-3 text-rust-dark">
              <span className="text-base sm:text-lg">{ingredient.ingredient__name}</span>
              <span className="text-base sm:text-lg font-medium shrink-0">{ingredient.quantity}</span>
            </li>
          ))}
        </ul>
      </section>

      {context["recipe"].directions ? (
        <section className="mt-8">
          <h2 className="font-display text-xl sm:text-2xl text-rust-dark mb-3">Directions</h2>
          <p className="rounded-2xl bg-cream-dark/60 px-4 sm:px-6 py-4 text-rust-dark whitespace-pre-line leading-relaxed">
            {context["recipe"].directions}
          </p>
        </section>
      ) : null}

      <section className="mt-10">
        <h2 className="font-display text-xl sm:text-2xl text-rust-dark mb-3">Comments</h2>
        {comments.length === 0 ? (
          <p className="text-rust-dark/70 py-6 text-center">No comments yet — be the first to say something.</p>
        ) : (
          <ul className="list-none">
            {comments.map((comment, index) => (
              <li
                key={`comment-${index}`}
                className="flex flex-col gap-1 py-3 border-b border-rust-dark/15 last:border-b-0"
              >
                <span className="text-rust-dark text-base leading-snug">{comment.content}</span>
                <span className="text-rust-dark/60 text-xs">{timeAgo(comment.created_at)}</span>
              </li>
            ))}
          </ul>
        )}
        <form onSubmit={handleCommentSubmit} className="mt-6 flex flex-col gap-3">
          <input type="hidden" name="csrfmiddlewaretoken" value={context["csrf_token"]} readOnly />
          <input type="hidden" name="recipe_id" value={context["recipe"].id} readOnly />
          <label htmlFor="comment" className="text-rust-dark font-medium">Add a comment</label>
          <Input type="text" id="comment" name="comment" required className="w-full" />
          <Button type="submit" className="self-start">Comment</Button>
        </form>
      </section>
    </div>
  );
}

export default RecipeView;
