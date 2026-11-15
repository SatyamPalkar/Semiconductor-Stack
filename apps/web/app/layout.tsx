import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "Semiconductor Research Platform", description: "Traceable research into where semiconductor value is created and captured. Historical financial pilot with source provenance." };
export default function RootLayout({ children }: { children: React.ReactNode }) { return <html lang="en"><body>{children}</body></html>; }
