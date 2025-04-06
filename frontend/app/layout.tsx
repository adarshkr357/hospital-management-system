// app/layout.tsx
import "@/app/globals.css";
import { ThemeProvider } from "@/app/components/ThemeContext";
import { UserProvider } from "@/app/components/UserContext";
import Navbar from "@/app/components/Navbar";
import { Toaster } from "react-hot-toast";
import Footer from "./components/Footer";

export const metadata = {
  title: "Hospital Management System",
  description: "A full stack hospital management system",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <UserProvider>
          <ThemeProvider>
            <Navbar />
            <main className="container mx-auto px-4 py-6">{children}</main>
            <Toaster position="top-right" />
            <Footer />
          </ThemeProvider>
        </UserProvider>
      </body>
    </html>
  );
}
