// Access-code handling. The code can arrive as ?k=CODE in the URL (e.g. a resume link).
// We stash it in sessionStorage and immediately scrub it from the URL, so it isn't left
// in the address bar, history, or a screenshot, then send it with each query.

const KEY = "answertrail_access_code";

// Call once on load: if the URL has ?k=CODE, save it and remove it from the URL.
export function captureAccessCode(): void {
  if (typeof window === "undefined") return;
  const url = new URL(window.location.href);
  const k = url.searchParams.get("k");
  if (k) {
    sessionStorage.setItem(KEY, k);
    url.searchParams.delete("k");
    window.history.replaceState({}, "", url.toString());
  }
}

export function getAccessCode(): string | undefined {
  if (typeof window === "undefined") return undefined;
  return sessionStorage.getItem(KEY) ?? undefined;
}
