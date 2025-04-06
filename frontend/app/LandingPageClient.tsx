// app/LandingPageClient.tsx (Client Component)
"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import type { Doctor, Testimonial } from "@/app/lib/getLandingData";

type LandingPageClientProps = {
  doctors: Doctor[];
  testimonials: Testimonial[];
};

export default function LandingPageClient({
  doctors,
  testimonials,
}: LandingPageClientProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, 100);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      <main className="flex-1">
        {/* Header Section */}
        <section
          className={`py-20 text-center shadow-xl transition-all duration-700 ${
            isVisible
              ? "opacity-100 translate-y-0"
              : "opacity-0 -translate-y-12"
          }`}
        >
          <h1
            className={`text-4xl font-bold mb-4 transition-opacity duration-500 ${
              isVisible ? "opacity-100" : "opacity-0"
            }`}
          >
            Welcome to the Hospital Management System
          </h1>
          <p
            className={`text-lg mb-8 transition-opacity delay-200 duration-500 ${
              isVisible ? "opacity-100" : "opacity-0"
            }`}
          >
            Your health, our priority. Streamline patient care with seamless
            management.
          </p>
          <Link
            href="/login"
            className="btn bg-gradient-to-r from-blue-500 to-indigo-600 hover:opacity-90 text-white font-bold px-8 py-4 rounded shadow-lg transition duration-300"
          >
            Get Started
          </Link>
        </section>

        <div className="divider mx-auto w-1/2 my-12"></div>

        {/* Featured Doctors Section */}
        <section className="py-16 px-4">
          <h2 className="text-3xl font-bold text-center mb-8">
            Featured Doctors
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
            {doctors.map((doctor, index) => (
              <div
                key={index}
                className="shadow-lg p-4 rounded text-center hover:scale-105 transition duration-200"
              >
                <img
                  src={doctor.image}
                  alt={doctor.name}
                  className="w-24 h-24 mx-auto rounded-full object-cover mb-4"
                />
                <h3 className="font-semibold">{doctor.name}</h3>
                <p>{doctor.specialty}</p>
              </div>
            ))}
          </div>
        </section>

        <div className="divider mx-auto w-1/2 my-12"></div>

        {/* Testimonials Section */}
        <section className="py-16 px-4">
          <h2 className="text-3xl font-bold text-center mb-8">
            What Our Patients Say
          </h2>
          <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="p-6 rounded shadow-lg text-center">
                <img
                  src={testimonial.image}
                  alt={testimonial.name}
                  className="w-16 h-16 rounded-full mx-auto mb-4 object-cover"
                />
                <p className="italic mb-4">"{testimonial.quote}"</p>
                <h4 className="font-bold text-blue-600">{testimonial.name}</h4>
              </div>
            ))}
          </div>
        </section>

        <div className="divider mx-auto w-1/2 my-12"></div>

        {/* Contact Section */}
        <section className="py-16 px-4">
          <h2 className="text-3xl font-bold text-center mb-8">Contact Us</h2>
          <div className="max-w-lg mx-auto">
            {submitted ? (
              <div className="text-center text-green-600 text-xl font-semibold">
                Thank you for reaching out!
              </div>
            ) : (
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  setSubmitted(true);
                }}
                className="space-y-4"
              >
                <div>
                  <label htmlFor="name" className="block">
                    Name
                  </label>
                  <input
                    id="name"
                    name="name"
                    type="text"
                    required
                    className="w-full border rounded px-3 py-2"
                  />
                </div>
                <div>
                  <label htmlFor="email" className="block">
                    Email
                  </label>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    required
                    className="w-full border rounded px-3 py-2"
                  />
                </div>
                <div>
                  <label htmlFor="message" className="block">
                    Message
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    required
                    rows={4}
                    className="w-full border rounded px-3 py-2"
                  ></textarea>
                </div>
                <button
                  type="submit"
                  className="btn bg-[#1A77F2] text-white border-[#005fd8] w-full font-bold py-2 px-4 rounded"
                >
                  Send Message
                </button>
              </form>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
