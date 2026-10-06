import Button from '../components/Button.jsx'
import Input from '../components/Input.jsx';
import blobs from '../images/riso/riso-blobs.svg';

function Signup({ context }) {
  return (
    <div className="relative isolate mx-auto max-w-2xl mt-20 px-4">
      <img src={blobs} alt="" aria-hidden="true" className="absolute left-1/2 top-1/2 -z-10 w-full -translate-x-1/2 -translate-y-1/2 pointer-events-none" />
      <div className="mx-auto max-w-sm rounded-xl shadow-md bg-sage p-10">
        <form action={`/accounts/signup/${context.code}`} method="POST" className="flex flex-col gap-y-4 items-center">
        <input type="hidden" name="csrfmiddlewaretoken" value={context["csrf_token"]}></input>
          <label>Username: <Input type="text" name="username" value={context.username} required/></label>
          <label>Password: <Input type="password" name="password1" required/></label>
          <label>Password Confirm: <Input type="password" name="password2" required/></label>
          <Button type="submit" >Sign Up</Button>
        </form>
        {context.error}
      </div>
    </div>
  );
}

export default Signup;