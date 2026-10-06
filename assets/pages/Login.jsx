import Button from '../components/Button.jsx'
import Input from '../components/Input.jsx';
import blobs from '../images/riso/riso-blobs.svg';

function Login({ context }) {
  const labelClassName = "flex flex-col gap-1 w-full font-display text-lg text-cream";
  const inputClassName = "w-full shadow-[2px_2px_0_var(--color-rust)]";
  return (
    <div className="relative isolate mx-auto max-w-2xl mt-20 px-4">
      <img src={blobs} alt="" aria-hidden="true" className="absolute left-1/2 top-1/2 -z-10 w-full -translate-x-1/2 -translate-y-1/2 pointer-events-none" />
      <div className="mx-auto max-w-sm rounded-xl shadow-md bg-sage bg-ink-speckle p-8 sm:p-10">
        <h1 className="font-display text-3xl text-cream text-center riso-offset mb-6">Welcome back</h1>
        <form action="/accounts/login" method="POST" className="flex flex-col gap-y-4 items-center">
          <input type="hidden" name="csrfmiddlewaretoken" value={context["csrf_token"]}></input>
          <label className={labelClassName}>
            Username
            <Input type="text" name="username" required className={inputClassName} />
          </label>
          <label className={labelClassName}>
            Password
            <Input type="password" name="password" required className={inputClassName} />
          </label>
          <Button type="submit" onDark className="mt-2">Log In</Button>
        </form>
      </div>
    </div>
  );
}

export default Login;
