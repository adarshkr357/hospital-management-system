export type Doctor = {
    name: string;
    specialty: string;
    image: string;
};

export type Testimonial = {
    name: string;
    quote: string;
    image: string;
};

export async function getLandingData(): Promise<{
    doctors: Doctor[];
    testimonials: Testimonial[];
}> {
    const unsplashKey = process.env.UNSPLASH_API_KEY;
    if (!unsplashKey) {
        throw new Error("Unsplash API key is missing");
    }

    // Fetch doctors data from Unsplash
    const doc_response = await fetch(
        `https://api.unsplash.com/search/photos?client_id=${unsplashKey}&query=Doctor`
    );
    const doc_data = await doc_response.json();
    const random = (min: number, max: number) =>
        Math.floor(Math.random() * (max - min + 1) + min);

    const doctors: Doctor[] = doc_data.results
        .sort(() => Math.random() - 0.5)
        .slice(0, 3)
        .map((result: any) => ({
            name: `Dr. ${result.user.name || "Unknown"}`,
            specialty: ["General Physician", "Neonatologist", "Cardiologist"].sort(
                () => Math.random() - 0.5
            )[random(0, 2)],
            image: result.user.profile_image.large,
        }));

    // Fetch patients data from Unsplash
    const user_response = await fetch(
        `https://api.unsplash.com/search/photos?client_id=${unsplashKey}&query=Patient`
    );
    const user_data = await user_response.json();
    const users: Testimonial[] = user_data.results
        .sort(() => Math.random() - 0.5)
        .slice(0, 3)
        .map((result: any) => ({
            name: result.user.name || "Unknown",
            quote: [
                "This hospital management system has streamlined our patient care. Highly recommend!",
                "An amazing solution for keeping our hospital operations efficient and transparent.",
                "User-friendly and comprehensive. It really transformed our workflow.",
            ].sort(() => Math.random() - 0.5)[random(0, 2)],
            image: result.user.profile_image.large,
        }));

    const testimonials = users.map((user) => ({
        name: user.name,
        quote: user.quote,
        image: user.image,
    }));

    return { doctors, testimonials };
}
