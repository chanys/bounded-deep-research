"use client";

// Persistent app shell: a slim sticky top bar shown on every route. Product name
// on the left (links home), nav on the right with the active route emphasized.

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  { href: "/query", label: "Query" },
  { href: "/system", label: "System" },
];

export function TopBar() {
  const pathname = usePathname();
  return (
    <header className="sticky top-0 z-10 border-b border-border bg-card/80 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-5xl items-center justify-between px-6">
        <Link href="/query" className="flex items-baseline gap-2">
          <span className="text-sm font-semibold tracking-tight">Bounded Deep Research</span>
          <span className="hidden text-xs text-muted-foreground sm:inline">
            bounded · traceable · cited
          </span>
        </Link>
        <nav className="flex items-center gap-5 text-sm">
          {NAV.map((n) => {
            const active = pathname === n.href;
            return (
              <Link
                key={n.href}
                href={n.href}
                className={
                  active
                    ? "font-medium text-foreground"
                    : "text-muted-foreground hover:text-foreground"
                }
              >
                {n.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
