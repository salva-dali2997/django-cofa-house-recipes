/**
 * Base className parameters: riso-style pink ink with a sage offset shadow, `py-3 px-6 rounded-full`
 * @param {string} [className] - Additional Tailwind classNames
 * @param {"button"|"submit"} [type="button"] - Default is button
 * @param {} [onClick] - Click handler, omit for submit button
 * @param {string} [children] - Children inside of the Button element
 * @param {string} [href] - Pass in an href to create an `<a>` with button styling
 * @param {boolean} [onDark=false] - Use a dark pink shadow so the offset still shows on sage backgrounds
*/

function Button({ type="button", className, onClick, children, href, onDark=false }) {
  // Riso look: speckled pink "ink" with a misregistered sage copy as a hard shadow.
  // On hover the button presses down into its shadow.
  const baseClasses = `inline-flex items-center justify-center min-h-11 py-3 px-6 rounded-full font-display tracking-wide
    bg-rust bg-ink-speckle text-cream hover:bg-rust-dark hover:translate-x-0.5 hover:translate-y-0.5
    ${onDark
      ? "shadow-[3px_3px_0_var(--color-rust-dark2)] hover:shadow-[1px_1px_0_var(--color-rust-dark2)]"
      : "shadow-[3px_3px_0_var(--color-sage)] hover:shadow-[1px_1px_0_var(--color-sage)]"}
    active:translate-x-[3px] active:translate-y-[3px] active:shadow-none transition-all
    focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-rust-dark`
  return (
    !href ?
      <button
        type={type}
        className={`${baseClasses} ${className || ""}`}
        onClick={onClick}
        >{children}
      </button> :
      <a
        className={`${baseClasses} ${className || ""}`}
        href={href}>{children}
      </a>
  )
}

export default Button;
