export default function Footer() {
    return (
      <footer
        className="shadow-xl p-4 text-center"
      >
        <p className="text-sm">
          &copy; {new Date().getFullYear()} Hospital Management. All rights
          reserved by{" "}
          <a
            href="https://www.linkedin.com/in/adarshkr357/"
            className="text-blue-500"
          >
            AdarshKr357
          </a>
          .
        </p>
      </footer>
    );
}