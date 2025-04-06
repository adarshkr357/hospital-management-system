export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-center p-4">
      <h1 className="text-4xl font-bold mb-4">404 - Page Not Found</h1>
      <p className="text-lg mb-6">
        Sorry, we couldn't find the page you're looking for.
      </p>
      <a href="/" className="btn btn-primary">
        Back to Home
      </a>
    </div>
  );
}
