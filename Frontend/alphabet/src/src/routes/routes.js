
/** 
  All of the routes for the Alphabet are added here,
  You can add a new route, customize the routes and delete the routes here.

  Once you add a new route on this file it will be visible automatically on
  the Sidenav.

  For adding a new route you can follow the existing routes in the routes array.
  1. The `type` key with the `collapse` value is used for a route.
  2. The `type` key with the `title` value is used for a title inside the Sidenav. 
  4. The `name` key is used for the name of the route on the Sidenav.
  5. The `key` key is used for the key of the route (It will help you with the key prop inside a loop).
  6. The `icon` key is used for the icon of the route on the Sidenav, you have to add a node.
  7. The `collapse` key is used for making a collapsible item on the Sidenav that has other routes
  inside (nested routes), you need to pass the nested routes inside an array as a value for the `collapse` key.
  8. The `route` key is used to store the route location which is used for the react router.
  9. The `href` key is used to store the external links location.
  10. The `component` key is used to store the component of its route.
  11 The 'subRoute' key is used to add the fragment routes.
*/
import { Navigate, useLocation } from "react-router-dom";
import cookiesManipulator from "../services/browserStorage/cookies";
import { lazy, Suspense } from "react";
import  Loader  from "../components/loader/index";
import ErrorBoundary from "../components/ErrorBoundary/ErrorBoundary";



const Profile = lazy(() => import("../containers/app/Profile"));
function LazyProfile(props) {
  return (
    <Suspense fallback={<Loader />}>
      <ErrorBoundary>
        <Profile {...props} />
      </ErrorBoundary>
    </Suspense>
  );
}


const routes = [
  {
    key: "profile",
    name: "Profile",
    route: "/",
    layout: "/app",
    component: <Profile />,
  },
];

export function RequireAuth({ children }) {
  const authed = !!cookiesManipulator.getAuth().token;
  const location = useLocation();
  return authed === true ? (
    children
  ) : (
    <Navigate to="/auths/login" replace state={{ path: location.pathname }} />
  );
}
export default routes;