import type {Metadata} from "next";
import {Geist, Geist_Mono} from "next/font/google";
import "./globals.css";

const geistSans = Geist({
    variable: "--font-geist-sans",
    subsets: ["latin"],
});

const geistMono = Geist_Mono({
    variable: "--font-geist-mono",
    subsets: ["latin"],
});

export const metadata: Metadata = {
    title: "Smart Search",
    description: "The better way to study",
};

export default function RootLayout({
                                       children,
                                   }: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
        <body
            className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        >

        <header className="fixed top-0 left-0 w-full">
            {/* Navigation Bar */}
            <nav className="bg-gray-800 text-white py-4 px-6 flex justify-between items-center">
                <div className="text-3xl font-bold">Smart Search</div>
                <div>
                    <a href="./" className="mx-4 hover:text-blue-500">
                        Home
                    </a>
                    <a href="./knowledge-manager" className="mx-4 hover:text-blue-500">
                        Knowledge Manager
                    </a>
                    <a href="./documentation" className="mx-4 hover:text-blue-500">
                        Documentation
                    </a>
                </div>
            </nav>
        </header>


        {/* Main Content */}
        <main className="pt-[4rem] flex-grow">
            {children}
        </main>

        </body>
        </html>
    );
}
