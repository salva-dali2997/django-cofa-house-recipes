import Button from '../components/Button.jsx'
import Input from '../components/Input.jsx';

function Signup({ context }) {
  return (
    <div className="mx-auto max-w-sm rounded-xl shadow-md bg-sage p-10 mt-20">
      <form action={`/accounts/signup/${context.code}`} method="POST" className="flex flex-col gap-y-4 items-center">
      <input type="hidden" name="csrfmiddlewaretoken" value={context["csrf_token"]}></input>
        <label>Username: <Input type="text" name="username" value={context.username} required/></label>
        <label>Password: <Input type="password" name="password1" required/></label>
        <label>Password Confirm: <Input type="password" name="password2" required/></label>
        <Button type="submit" >Sign Up</Button>
      </form>
      {context.error}
    </div>
  );
}

export default Signup;