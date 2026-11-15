import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
const barlow = localFont({ src: [{ path: "./fonts/Barlow-Regular.ttf", weight: "400", style: "normal" }, { path: "./fonts/Barlow-SemiBold.ttf", weight: "600", style: "normal" }], variable: "--font-barlow", display: "swap" });
export const metadata: Metadata = { title: "semiscope — The Silicon Atlas", description: "Explore 139 semiconductor companies and businesses, 36 official research resources, and six historical financial datasets with visual cash analysis and source evidence." };
export default function RootLayout({ children }: { children: React.ReactNode }) { return <html lang="en" className={barlow.variable}><body>{children}</body></html>; }
