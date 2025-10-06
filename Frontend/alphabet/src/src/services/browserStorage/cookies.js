// Simple cookie helper specialized for auth token storage

const COOKIE_KEY = "auth_token";
const COOKIE_MAX_AGE_DAYS = 7;

function setCookie(name, value, days) {
  const date = new Date();
  date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
  const expires = "; expires=" + date.toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value || "")}${expires}; path=/`;
}

function getCookie(name) {
  const nameEQ = name + "=";
  const ca = document.cookie.split(";");
  for (let i = 0; i < ca.length; i += 1) {
    let c = ca[i];
    while (c.charAt(0) === " ") c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) === 0) return decodeURIComponent(c.substring(nameEQ.length, c.length));
  }
  return "";
}

function eraseCookie(name) {
  document.cookie = `${name}=; Max-Age=0; path=/`;
}

const cookiesManipulator = {
  setAuth: (token) => setCookie(COOKIE_KEY, token, COOKIE_MAX_AGE_DAYS),
  getAuth: () => ({ token: getCookie(COOKIE_KEY) }),
  clearAuth: () => eraseCookie(COOKIE_KEY),
};

export default cookiesManipulator;


