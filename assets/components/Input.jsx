/**
 * Base className parameters: `border border-black py-2 px-4 rounded-full`
 * @param {string} [className] - Additional Tailwind classNames
 * @param {"text"|"password"} [type="text"] - Default is text
 * @param {string} [id] - Id for the input
 * @param {string} [name] - Name of the input field
 * @param {string} [children] - Children inside of the Button element
 * @param {boolean} [required] - Whether the field is required on submit
*/

function Input({ className, type="text", name, children, required, id }) {
  const baseClasses = "py-2 px-4 border-b-2 rounded-md focus:outline-none focus:ring-2 focus:ring-rust bg-cream"
  return (
    <input 
      className={`${baseClasses} ${className || ""}`}
      type={type}
      name={name}
      required={required}
      id={id}
      >{children}
    </input>
  )
}

export default Input;