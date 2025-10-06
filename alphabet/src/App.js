import { useState, useEffect } from "react";
import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import routes, { RequireAuth } from "./src/routes/routes";
import cookiesManipulator from "./src/services/browserStorage/cookies";

import DashboardNavbar from "./src/modules/Navbar/index";
import Sidenav from "./src/modules/Sidenav";
import Profile from "./src/containers/app/Profile";

function App() {
  const location = useLocation();
  const pathname = location.pathname;

  const [sidebarOpen, setSidebarOpen] = useState(false); // for mobile
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false); // for desktop mini mode

  // build routes dynamically
  const getRoutes = (allRoutes, parentRoute = "") =>
    allRoutes.flatMap((route) => {
      const { route: currentRoute, layout, component, subRoutes } = route;
      const fullRoute = parentRoute + (currentRoute || "");
      const routePath = (layout || "") + fullRoute;

      const routeComponent = component && (
        <Route
          exact
          path={routePath}
          element={<RequireAuth>{component}</RequireAuth>}
          key={route.key}
        />
      );

      if (subRoutes && subRoutes.length > 0) {
        const subRoutesComponents = getRoutes(subRoutes, fullRoute);
        return [routeComponent, ...subRoutesComponents];
      }

      return routeComponent;
    });

  // reset scroll on route change
  useEffect(() => {
    document.documentElement.scrollTop = 0;
    if (document.scrollingElement) document.scrollingElement.scrollTop = 0;
  }, [pathname]);

  const isAuthed = !!cookiesManipulator.getAuth().token;

  const handleLogout = () => {
    cookiesManipulator.clearAuth();
    window.location.href = "/app";
  };

  return (
    <>
      <DashboardNavbar
        isAuthed={isAuthed}
        onToggleSidebar={() => {
          if (window.innerWidth < 900) {
            setSidebarOpen((o) => !o);
          } else {
            setSidebarCollapsed((c) => !c);
          }
        }}
        onLogout={handleLogout}
      />

      <Sidenav
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        collapsed={sidebarCollapsed}
        routes={routes}
      />

      <div className={`app-content ${sidebarCollapsed ? "collapsed" : ""}`}>
        <Routes>
          {getRoutes(routes)}

       
          <Route path="/app" element={<Profile />} />

         
          <Route path="*" element={<Navigate to="/app" replace />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
