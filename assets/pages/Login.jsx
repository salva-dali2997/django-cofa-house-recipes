import Button from '../components/Button.jsx'
import Input from '../components/Input.jsx';

function Login({ context }) {
  return (
    <div className="mx-auto max-w-sm rounded-xl shadow-md bg-sage p-10 mt-20">
      <form action="/accounts/login" method="POST" className="flex flex-col gap-y-4 items-center">
      <input type="hidden" name="csrfmiddlewaretoken" value={context["csrf_token"]}></input>
        <label>Username: <Input type="text" name="username" required/></label>
        <label>Password: <Input type="password" name="password" required/></label>
        {/* <button type="submit">Log In</button> */}
        <Button type="submit">Log In</Button>
      </form>
    </div>
  );
}

export default Login;