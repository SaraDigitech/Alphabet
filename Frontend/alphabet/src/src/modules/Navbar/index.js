export default function Navbar({ isAuthed = false, onToggleSidebar, onLogin, onRegister }) {
return (
<header className="alphabet-navbar" role="navigation" aria-label="Main navigation">
      <button
        className="nav-hamburger"
        aria-label="Open menu"
        onClick={onToggleSidebar}
        type="button"
      >
        <span />
        <span />
        <span />
      </button>

      <div className="nav-left">
        <div className="nav-pill-group" role="group" aria-label="Sections">
          <button className="pill" type="button">Casino</button>
          <button className="pill" type="button">Poker</button>
        </div>
      </div>

      <div className="nav-center">
        <div className="brand">Alphabet</div>
      </div>

      <div className="nav-right">
        {/* If user is authenticated you could show profile/avatar instead */}
        {!isAuthed && (
          <>
            <button className="ghost" onClick={onLogin} type="button">Login</button>
            <button className="cta" onClick={onRegister} type="button">Register</button>
          </>
        )}

        {isAuthed && (
          <button className="cta" type="button">My Account</button>
        )}
      </div>
    </header>
);
}