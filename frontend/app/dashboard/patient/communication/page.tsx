"use client";
import { useState } from "react";
import toast from "react-hot-toast";

interface Communication {
  id: number;
  type: "sms" | "email";
  subject: string;
  message: string;
  sentAt: string;
}

export default function PatientCommunication() {
  const [type, setType] = useState<"sms" | "email">("sms");
  const [subject, setSubject] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [communications, setCommunications] = useState<Communication[]>([]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validate fields: if email is selected, subject must not be empty.
    if (type === "email" && subject.trim() === "") {
      toast.error("Subject is required for email communications");
      return;
    }
    if (message.trim() === "") {
      toast.error("Message is required");
      return;
    }

    // Create a new communication object
    const newComm: Communication = {
      id: Date.now(),
      type,
      subject: type === "email" ? subject : "",
      message,
      sentAt: new Date().toLocaleString(),
    };

    // For demo purposes, we'll simply update our local state
    setCommunications([newComm, ...communications]);
    toast.success("Message sent successfully!");

    // Clear the form fields
    setSubject("");
    setMessage("");
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Communication</h1>
      <p>
        This section allows you to send SMS or Email updates such as test
        results and follow-up reminders.
      </p>

      {/* Communication form */}
      <form onSubmit={handleSubmit} className="space-y-4 border p-4 rounded-lg">
        <div>
          <label htmlFor="type" className="label">
            Communication Type
          </label>
          <select
            id="type"
            value={type}
            onChange={(e) => setType(e.target.value as "sms" | "email")}
            className="select select-bordered w-full"
          >
            <option value="sms">SMS</option>
            <option value="email">Email</option>
          </select>
        </div>

        {type === "email" && (
          <div>
            <label htmlFor="subject" className="label">
              Subject
            </label>
            <input
              id="subject"
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="Enter email subject"
              className="input input-bordered w-full"
              required
            />
          </div>
        )}

        <div>
          <label htmlFor="message" className="label">
            Message
          </label>
          <textarea
            id="message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Enter your message"
            className="textarea textarea-bordered w-full"
            required
          ></textarea>
        </div>

        <button type="submit" className="btn btn-primary">
          Send Message
        </button>
      </form>

      {/* Past communications list */}
      <div className="space-y-4">
        <h2 className="text-2xl font-semibold">Past Communications</h2>
        {communications.length === 0 ? (
          <p>No communications sent yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="table w-full">
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Subject</th>
                  <th>Message</th>
                  <th>Sent At</th>
                </tr>
              </thead>
              <tbody>
                {communications.map((comm) => (
                  <tr key={comm.id}>
                    <td>{comm.type.toUpperCase()}</td>
                    <td>{comm.type === "email" ? comm.subject : "-"}</td>
                    <td>{comm.message}</td>
                    <td>{comm.sentAt}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
