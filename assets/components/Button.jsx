/**
 * Base className parameters: `border border-black py-2 px-4 rounded-full`
 * @param {string} [className] - Additional Tailwind classNames
 * @param {"button"|"submit"} [type="button"] - Default is button
 * @param {} [onClick] - Click handler, omit for submit button
 * @param {string} [children] - Children inside of the Button element
 * @param {string} [href] - Pass in an href to create an `<a>` with button styling
*/

function Button({ type="button", className, onClick, children, href }) {
  const baseClasses = "bg-dark-salmon hover:bg-rust hover:text-cream py-2 px-4 rounded-full"
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