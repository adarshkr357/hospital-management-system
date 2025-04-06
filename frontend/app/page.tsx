// app/page.tsx (Server Component)
import { getLandingData } from "@/app/lib/getLandingData";
import LandingPageClient from "@/app/LandingPageClient";

export default async function LandingPage() {
  // Fetch data on the server; the API key remains hidden
  const { doctors, testimonials } = await getLandingData();

  return <LandingPageClient doctors={doctors} testimonials={testimonials} />;
}
