import { getCookie, setCookie, type OptionsType } from "cookies-next";

export const SESSION_COOKIE = "VITTAM_SESSION";
export const COOKIE_OPTIONS: OptionsType = {
  path: "/",
  maxAge: 60 * 60 * 24 * 30,
  secure: process.env.NODE_ENV === "production",
};

export const setSessionCookie = async (data: { id: string; email: string; name: string }) => {
  await setCookie(SESSION_COOKIE, data, COOKIE_OPTIONS);
};

export const getSessionCookie = async () => {
  return await getCookie(SESSION_COOKIE, COOKIE_OPTIONS);
};
