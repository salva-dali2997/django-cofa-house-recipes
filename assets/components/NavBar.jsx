import { useState } from 'react';
import Logo from './Logo.jsx'

function NavBar({ context }){
  const navList = [
    {text: "All Recipes", href: "/recipes/", visibility: "always"},
    {text: "Today's Recipes", href: "/recipes/today", visibility: "always"},
    {text: "Login", href: "/accounts/login", visibility: "anonymous"},
    {text: "Create Recipe", href: "/recipes/create", visibility: "authenticated"},
    {text: "Logout", href: "/accounts/logout-confirm", visibility: "authenticated"},
  ];
  const isAuthenticated = context["user_authenticated"];
  const filteredNavList = navList.filter(item => item.visibility === "always" || (item.visibility === "authenticated") === isAuthenticated);
  const desktopLinkClassName = "flex items-center justify-center hover:bg-sage-dark rounded-xl p-1 pb-2";
  const mobileLinkClassName = "block py-2 hover:bg-sage-dark px-2 rounded";
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  return (
  <>
  <nav className="bg-sage bg-noise text-cream text-outline flex flex-row justify-between items-center p-10">
    <div className="container mx-auto px-4">
      {/* left hand side div */}
      <div className="flex flex-row items-center justify-between gap-x-10 xl:gap-x-20 gap-y-2">
        <div className="flex flex-col lg:flex-row items-center gap-x-20">
          <Logo className="w-30 max-w-full text-rust-dark2"></Logo>
          <h1 className="text-xl md:text-2xl lg:text-4xl font-bold">Cofa House Recipes</h1>
        </div>
        <button id="menu-btn" className="md:hidden" onClick={() => setIsMenuOpen((prev) => !prev)}>
          <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        {/* right hand side div */}
        <div className="hidden md:flex flex-row justify-center gap-x-4 lg:gap-x-20 text-2xl lg:text-3xl">
          {filteredNavList.map((navElement, index) => {
            return (
              <a key={index} href={navElement.href} className={desktopLinkClassName}>{navElement.text}</a>
            );
          })}
        </div>
      </div>
      <div id="mobile-menu" className={`fixed top-0 right-0 h-full w-40 z-50 bg-sage transition-transform duration-300 text-3xl ${!isMenuOpen ? "translate-x-full" : "translate-x-0"}`}>
          {filteredNavList.map((navElement, index) => {
            return (
              <a key={index} href={navElement.href} className={mobileLinkClassName}>{navElement.text}</a>
            );
          })}
      </div>
    </div>
  </nav>
  {/* gradient */}
  <div className="nav-fade h-2 w-full mb-5 bg-noise"></div>
  </>
)};

export default NavBar;