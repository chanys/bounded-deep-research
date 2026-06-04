"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

// The app has no separate landing page; / sends you straight to the query UI.
// This is a client-side redirect (not the server `redirect()`), because the app is
// built as a static export with no server at runtime to issue an HTTP redirect.
// `replace` (not `push`) so the Back button doesn't bounce the user through / again.
export default function Home() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/query");
  }, [router]);
  return null;
}
