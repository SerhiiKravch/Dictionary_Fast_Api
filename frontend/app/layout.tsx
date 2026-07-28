import type { Metadata } from "next";
import Link from "next/link";

import "./globals.css";

export const metadata: Metadata = {
  title: "Dictionary Frontend",
  description: "Frontend scaffold for the dictionary project.",
};

type RootLayoutProps = Readonly<{
  children: React.ReactNode;
}>;

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en">
      <body>
        <div className="site-shell">
          <header className="site-header">
            <div className="site-header__inner">
              <Link href="/" className="site-brand">
                Dictionary
              </Link>
              <nav className="site-nav" aria-label="Primary">
                <Link href="/">Search</Link>
                <Link href="/words">Browse</Link>
                <Link href="/words/new">Add word</Link>
              </nav>
            </div>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
