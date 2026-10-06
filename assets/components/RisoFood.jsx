import tomato from '../images/riso/riso-tomato.svg';
import grapefruit from '../images/riso/riso-grapefruit.svg';
import mushroom from '../images/riso/riso-mushroom.svg';
import chili from '../images/riso/riso-chili.svg';

const FOODS = { tomato, grapefruit, mushroom, chili };
const FOOD_NAMES = Object.keys(FOODS);

// Deterministic pick so a recipe keeps the same doodle across page loads.
export function foodForId(id) {
  return FOOD_NAMES[id % FOOD_NAMES.length];
}

// Purely decorative, so it's hidden from screen readers.
function RisoFood({ food, className = "" }) {
  return (
    <img
      src={FOODS[food]}
      alt=""
      aria-hidden="true"
      draggable="false"
      className={`pointer-events-none select-none ${className}`}
    />
  );
}

export default RisoFood;
