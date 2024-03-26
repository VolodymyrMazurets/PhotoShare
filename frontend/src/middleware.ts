import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { cookies } from "next/headers";

export function middleware(request: NextRequest) {
  const cookieStore = cookies();
  const loggedIn = cookieStore.get("token")?.value;
  
  const pathname = request.nextUrl.pathname;

  const authPathList = [
    "/login",
    "/signup",
    "/confirm-email",
    "/forgot-password",
    "/reset-password",
  ];

  if (!authPathList.includes(pathname) && !loggedIn) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (authPathList.includes(pathname) && loggedIn) {
    return NextResponse.redirect(new URL("/", request.url));
  }
}

export const config = {
  matcher: ["/"],
};
