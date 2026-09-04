import Logo from './Logo.jsx'

function NavBar(){
  return (
  <>
  <nav className="bg-sage bg-noise text-cream text-outline flex flex-row justify-between items-center p-10">
    {/* left hand side div */}
    <div className="flex flex-row items-center gap-x-20">
      <Logo className="w-30 max-w-full text-rust"></Logo>
      <h1 className="text-4xl text-bold">Cofa House Recipes</h1>
    </div>
    {/* right hand side div */}
    <div className="flex flex-row gap-x-20 text-3xl">
      <a href="/recipes/">All Recipes</a>
      <a href="/recipes/create">Create Recipe</a>
      <a href="/accounts/login">Login</a>
      <a href="/accounts/logout-confirm">Logout</a>
    </div>
  </nav>
  {/* gradient */}
  <div className="nav-fade h-2 w-full mb-5 bg-noise"></div>
  </>
)};

export default NavBar;