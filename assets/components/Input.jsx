/**
 * Base className parameters: `min-h-11 py-2 px-4 border-b-2 border-rust-dark/30 rounded-md focus:outline-none focus:ring-2 focus:ring-rust bg-cream font-sans text-rust-dark`
 * @param {string} [className] - Additional Tailwind classNames
 * @param {"text"|"password"} [type="text"] - Default is text
 * @param {string} [id] - Id for the input
 * @param {string} [name] - Name of the input field
 * @param {string} [placeholder] - Placeholder text
 * @param {string} [value] - Controlled value
 * @param {string} [defaultValue] - Uncontrolled initial value
 * @param {function} [onChange] - Change handler
 * @param {boolean} [required] - Whether the field is required on submit
*/

function Input({ className, type="text", name, placeholder, value, defaultValue, onChange, required, id }) {
  // font-sans/text-rust-dark are explicit because Tailwind's preflight makes inputs inherit
  // font and color, which breaks inputs nested in styled labels (e.g. cream display-font labels).
  const baseClasses = "min-h-11 py-2 px-4 border-b-2 border-rust-dark/30 rounded-md focus:outline-none focus:ring-2 focus:ring-rust bg-cream text-base font-sans text-rust-dark"
  return (
    <input
      className={`${baseClasses} ${className || ""}`}
      type={type}
      name={name}
      placeholder={placeholder}
      value={value}
      defaultValue={defaultValue}
      onChange={onChange}
      required={required}
      id={id}
      />
  )
}

export default Input;
