// app/components/AppointmentForm.tsx
"use client";
import { useState, FormEvent } from "react";

interface AppointmentFormData {
  patientId: number;
  doctorId: number;
  appointmentDate: string;
  purpose: string;
  notes?: string;
}

interface AppointmentFormProps {
  initialData?: AppointmentFormData;
  onSubmit: (data: AppointmentFormData) => void;
}

export default function AppointmentForm({
  initialData,
  onSubmit,
}: AppointmentFormProps) {
  const [formData, setFormData] = useState<AppointmentFormData>(
    initialData || {
      patientId: 0,
      doctorId: 0,
      appointmentDate: "",
      purpose: "",
      notes: "",
    }
  );

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="patientId" className="label">
          Patient ID
        </label>
        <input
          type="number"
          id="patientId"
          name="patientId"
          value={formData.patientId}
          onChange={handleChange}
          className="input input-bordered w-full"
          required
        />
      </div>
      <div>
        <label htmlFor="doctorId" className="label">
          Doctor ID
        </label>
        <input
          type="number"
          id="doctorId"
          name="doctorId"
          value={formData.doctorId}
          onChange={handleChange}
          className="input input-bordered w-full"
          required
        />
      </div>
      <div>
        <label htmlFor="appointmentDate" className="label">
          Appointment Date
        </label>
        <input
          type="datetime-local"
          id="appointmentDate"
          name="appointmentDate"
          value={formData.appointmentDate}
          onChange={handleChange}
          className="input input-bordered w-full"
          required
        />
      </div>
      <div>
        <label htmlFor="purpose" className="label">
          Purpose
        </label>
        <input
          type="text"
          id="purpose"
          name="purpose"
          value={formData.purpose}
          onChange={handleChange}
          className="input input-bordered w-full"
          required
        />
      </div>
      <div>
        <label htmlFor="notes" className="label">
          Notes
        </label>
        <textarea
          id="notes"
          name="notes"
          value={formData.notes}
          onChange={handleChange}
          className="textarea textarea-bordered w-full"
        ></textarea>
      </div>
      <button type="submit" className="btn btn-primary">
        Submit
      </button>
    </form>
  );
}
