/* eslint-disable camelcase */
import getBrowserFingerprint from "get-browser-fingerprint";
import cookiesManipulator from "services/browserStorage/cookies";

const axios = require("axios");

export const API_URL = process.env.REACT_APP_API_URL;

export const getIdentity = async () => {
  const identifier = await getBrowserFingerprint({
    enableWebgl: true,
  });
  return identifier.toString();
};

let headers = {
  "x-origin": 1, // not allowed in cors
  "x-version": 1,
  "x-platform": 1, // not allowed in cors
  // "x-device-id": 1, // not allowed in cors
  "Content-Type": "application/json",
};

const requestApi = async (resourcePath, method, params, AdditionalHeaders = {}) => {
  headers["x-auth"] = await cookiesManipulator.getAuth().token;
  headers["x-device-id"] = await getIdentity();
  headers = {
    ...headers,
    ...AdditionalHeaders,
  };
  if (resourcePath.includes("auths") && !resourcePath.includes("logout")) {
    delete headers["x-auth"];
  }
  let response;
  if (["POST", "PUT", "DELETE"].indexOf(method) > -1 && params) {
    response = await axios({ url, method, data: params, headers });
    if (response.data.code === "authr_fail") {
      await cookiesManipulator.removeAuth();
      window.location.href = "/";
    }
    return response.data;
  }
  response = await axios({ url, method, headers });
  if (response.data.code === "authn_fail") {
    await cookiesManipulator.removeAuth();
    window.location.href = "/";
  }
  return response.data;
};

export default requestApi;