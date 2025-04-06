// app/components/PatientForm.tsx
"use client";
import { useState, FormEvent } from "react";

interface PatientFormData {
  fullName: string;
  dateOfBirth: string;
  gender: string;
  bloodGroup: string;
  contactNumber: string;
  email: string;
  address: string;
  emergencyContactName: string;
  emergencyContactNumber: string;
  insuranceProvider?: string;
  insuranceId?: string;
}

interface PatientFormProps {
  initialData?: PatientFormData;
  onSubmit: (data: PatientFormData) => void;
}

export default function PatientForm({
  initialData,
  onSubmit,
}: PatientFormProps) {
  const [formData, setFormData] = useState<PatientFormData>(
    initialData || {
      fullName: "",
      dateOfBirth: "",
      gender: "",
      bloodGroup: "",
      contactNumber: "",
      email: "",
      address: "",
      emergencyContactName: "",
      emergencyContactNumber: "",
      insuranceProvider: "",
      insuranceId: "",
    }
  );

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
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
        <label htmlFor="fullName" className="label">
          Full Name
        </label>
        <input
          type="text"
          id="fullName"
          name="fullName"
          value={formData.fullName}
          onChange={handleChange}
          className="input input-bordered w-full"
          required
        />
      </div>

      <div>
        <label htmlFor="dateOfBirth" className="label">
          Date of Birth
        </label>
        <input
          type="date"
          id="dateOfBirth"
          name="dateOfBirth"
          value={formData.dateOfBirth}
          onChange={handleChange}
          className="input input-bordered w-full"
          required
        />
      </div>

      <div>
        <label htmlFor="gender" className="label">
          Gender
        </label>
        <select
          id="gender"
          name="gender"
          value={formData.gender}
          onChange={handleChange}
          className="select select-bordered w-full"
          required
        >
          <option value="">Select gender</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div>
        <label htmlFor="bloodGroup" className="label">
          Blood Group
        </label>
        <input
          type="text"
          id="bloodGroup"
          name="bloodGroup"
          value={formData.bloodGroup}
          onChange={handleChange}
          className="input input-bordered w-full"
        />
      </div>

      <div>
        <label htmlFor="contactNumber" className="label">
          Contact Number
        </label>
        <input
          type="text"
          id="contactNumber"
          name="contactNumber"
          value={formData.contactNumber}
          onChange={handleChange}
          className="input input-bordered w-full"
          required
        />
      </div>

      <div>
        <label htmlFor="email" className="label">
          Email
        </label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          className="input input-bordered w-full"
          required
        />
      </div>

      <div>
        <label htmlFor="address" className="label">
          Address
        </label>
        <textarea
          id="address"
          name="address"
          value={formData.address}
          onChange={handleChange}
          className="textarea textarea-bordered w-full"
          required
        ></textarea>
      </div>

      <div>
        <label htmlFor="emergencyContactName" className="label">
          Emergency Contact Name
        </label>
        <input
          type="text"
          id="emergencyContactName"
          name="emergencyContactName"
          value={formData.emergencyContactName}
          onChange={handleChange}
          className="input input-bordered w-full"
          required
        />
      </div>

      <div>
        <label htmlFor="emergencyContactNumber" className="label">
          Emergency Contact Number
        </label>
        <input
          type="text"
          id="emergencyContactNumber"
          name="emergencyContactNumber"
          value={formData.emergencyContactNumber}
          onChange={handleChange}
          className="input input-bordered w-full"
          required
        />
      </div>

      <div>
        <label htmlFor="insuranceProvider" className="label">
          Insurance Provider
        </label>
        <input
          type="text"
          id="insuranceProvider"
          name="insuranceProvider"
          value={formData.insuranceProvider}
          onChange={handleChange}
          className="input input-bordered w-full"
        />
      </div>

      <div>
        <label htmlFor="insuranceId" className="label">
          Insurance ID
        </label>
        <input
          type="text"
          id="insuranceId"
          name="insuranceId"
          value={formData.insuranceId}
          onChange={handleChange}
          className="input input-bordered w-full"
        />
      </div>

      <button type="submit" className="btn btn-primary">
        Submit
      </button>
    </form>
  );
}
