import React from "react";

 function Sidenav() {
  const menu = [
    { title: "Favourites", icon: "" },
    { title: "Recent", icon: "" },
    { title: "Challenges", icon: "" },
    { title: "My Game Play", icon: "" },
    "divider",
    { section: "Games" },
    { title: "New Releases", icon: "" },
    { title: "Slot Games", icon: "" },
    { title: "Stake Originals", icon: "" },
    { title: "Only on Stake", icon: "" },
    { title: "Live Dealers", icon: "" },
    { title: "Burst Games", icon: "" },
    { title: "Stake Poker", icon: "" },
    { title: "Feature Spins", icon: "" },
    { title: "Table Games", icon: "" },
    { title: "Scratch Cards", icon: "" },
    "divider",
    { title: "Promotions", icon: "" },
    { title: "Blog", icon: "" },
  ];

  return (
    <aside className="sidenav">
      <nav className="sidenav-content">
        {menu.map((item, idx) => {
          if (item === "divider")
            return <hr className="sidenav-divider" key={idx} />;
          if (item.section)
            return (
              <div className="sidenav-section" key={idx}>
                {item.section}
              </div>
            );
          return (
            <button key={idx} className="sidenav-item">
              <span className="sidenav-icon">{item.icon}</span>
              <span className="sidenav-label">{item.title}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}
export default Sidenav