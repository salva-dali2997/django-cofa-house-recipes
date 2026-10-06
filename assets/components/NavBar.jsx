import { useState } from 'react';
import Logo from './Logo.jsx'

function NavBar({ context }){
  const navList = [
    {text: "All Recipes", href: "/recipes/", visibility: "always"},
    {text: "Today's Recipes", href: "/recipes/today", visibility: "always"},
    {text: "Login", href: "/accounts/login", visibility: "anonymous"},
    {text: "Create Recipe", href: "/recipes/create", visibility: "authenticated"},
    {text: "Manage Menu", href: "/recipes/today/manage", visibility: "superuser"},
    {text: "Logout", href: "/accounts/logout-confirm", visibility: "authenticated"},
  ];
  const isAuthenticated = context["user_authenticated"];
  const isSuperuser = context["user_is_superuser"];
  const visibilityChecks = {
    always: true,
    anonymous: !isAuthenticated,
    authenticated: isAuthenticated,
    superuser: isSuperuser,
  };
  const filteredNavList = navList.filter(item => visibilityChecks[item.visibility]);
  const desktopLinkClassName = "font-display riso-link flex items-center justify-center px-1 pt-1";
  const mobileLinkClassName = "font-display block min-h-11 flex items-center px-6 text-xl hover:bg-sage-dark";
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  return (
  <>
  <nav className="bg-sage bg-ink-speckle text-cream flex flex-row items-center justify-between gap-4 px-4 py-3 sm:px-6 lg:px-10 lg:py-6">
    <a href="/recipes/" className="flex items-center gap-3 min-w-0">
      <Logo className="w-10 sm:w-14 lg:w-20 shrink-0 text-cream riso-offset"></Logo>
      <span className="font-display text-lg sm:text-2xl lg:text-4xl font-bold truncate riso-offset">Cofa House Recipes</span>
    </a>
    <button
      id="menu-btn"
      aria-label="Toggle navigation menu"
      aria-expanded={isMenuOpen}
      className="md:hidden shrink-0 flex items-center justify-center w-11 h-11 rounded-lg hover:bg-sage-dark focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cream"
      onClick={() => setIsMenuOpen((prev) => !prev)}
    >
      <svg className="w-7 h-7 riso-offset" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>
    <div className="hidden md:flex flex-row items-center gap-x-4 lg:gap-x-10 text-lg lg:text-2xl shrink-0">
      {filteredNavList.map((navElement, index) => (
        <a key={index} href={navElement.href} className={desktopLinkClassName}>{navElement.text}</a>
      ))}
    </div>
  </nav>
  {isMenuOpen ? (
    <button
      aria-label="Close navigation menu"
      className="md:hidden fixed inset-0 z-40 bg-black/40"
      onClick={() => setIsMenuOpen(false)}
    ></button>
  ) : null}
  <div
    id="mobile-menu"
    className={`md:hidden fixed top-0 right-0 h-full w-64 max-w-[80vw] z-50 bg-sage bg-ink-speckle shadow-xl transition-transform duration-300 py-6 ${!isMenuOpen ? "translate-x-full" : "translate-x-0"}`}
  >
    <div className="flex flex-col text-cream">
      {filteredNavList.map((navElement, index) => (
        <a key={index} href={navElement.href} className={mobileLinkClassName}>{navElement.text}</a>
      ))}
    </div>
  </div>
  {/* riso wavy edge */}
  <div aria-hidden="true" className="riso-nav-edge w-full mb-3"></div>
  </>
)};

export default NavBar;
