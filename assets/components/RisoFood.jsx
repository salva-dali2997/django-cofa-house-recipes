import { FOODS } from './risoFoods.js';

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
