// app/patient/page.tsx
"use client";
import { useState, useEffect, JSX } from "react";
import type { Patient, MedicalRecord, Appointment, Admission } from "../types";

export default function PatientDashboard(): JSX.Element {
  // States remain the same
  const [patientData, setPatientData] = useState<Patient | null>(null);
  const [medicalRecords, setMedicalRecords] = useState<MedicalRecord[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [admissionStatus, setAdmissionStatus] = useState<Admission | null>(
    null
  );
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch patient data
  const fetchPatientData = async (): Promise<void> => {
    try {
      const response = await fetch("http://localhost:8000/api/patient/details");
      if (!response.ok) throw new Error("Failed to fetch patient data");
      const data = await response.json();
      setPatientData(data);
    } catch (error) {
      setError("Failed to fetch patient data");
      console.error("Failed to fetch patient data:", error);
    }
  };

  // Fetch appointments
  const fetchAppointments = async (): Promise<void> => {
    try {
      const response = await fetch(
        "http://localhost:8000/api/patient/appointments"
      );
      if (!response.ok) throw new Error("Failed to fetch appointments");
      const data = await response.json();
      setAppointments(data);
    } catch (error) {
      setError("Failed to fetch appointments");
      console.error("Failed to fetch appointments:", error);
    }
  };

  // Fetch medical records
  const fetchMedicalRecords = async (): Promise<void> => {
    try {
      const response = await fetch(
        "http://localhost:8000/api/patient/medical-records"
      );
      if (!response.ok) throw new Error("Failed to fetch medical records");
      const data = await response.json();
      setMedicalRecords(data);
    } catch (error) {
      setError("Failed to fetch medical records");
      console.error("Failed to fetch medical records:", error);
    }
  };

  // Fetch admission status
  const fetchAdmissionStatus = async (): Promise<void> => {
    try {
      const response = await fetch(
        "http://localhost:8000/api/patient/admission-status"
      );
      if (!response.ok) throw new Error("Failed to fetch admission status");
      const data = await response.json();
      setAdmissionStatus(data);
    } catch (error) {
      setError("Failed to fetch admission status");
      console.error("Failed to fetch admission status:", error);
    }
  };

  // Handle new appointment booking
  const handleAppointmentBooking = async (
    e: React.FormEvent<HTMLFormElement>
  ): Promise<void> => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    const appointmentData: Partial<Appointment> = {
      appointmentDate: new Date(formData.get("date") as string),
      doctorId: formData.get("doctorId") as string,
      purpose: formData.get("purpose") as string,
      status: "SCHEDULED",
    };

    try {
      const response = await fetch("http://localhost:8000/api/appointments", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(appointmentData),
      });

      if (!response.ok) throw new Error("Failed to book appointment");
      await fetchAppointments();
    } catch (error) {
      setError("Failed to book appointment");
      console.error("Failed to book appointment:", error);
    }
  };

  // Handle appointment cancellation
  const handleAppointmentCancellation = async (
    appointmentId: string
  ): Promise<void> => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/appointments/${appointmentId}`,
        {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ status: "CANCELLED" }),
        }
      );

      if (!response.ok) throw new Error("Failed to cancel appointment");
      await fetchAppointments();
    } catch (error) {
      setError("Failed to cancel appointment");
      console.error("Failed to cancel appointment:", error);
    }
  };

  // Initial data fetch
  useEffect(() => {
    const fetchAllData = async () => {
      setLoading(true);
      try {
        await Promise.all([
          fetchPatientData(),
          fetchAppointments(),
          fetchMedicalRecords(),
          fetchAdmissionStatus(),
        ]);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAllData();
  }, []);

  if (loading)
    return (
      <div className="min-h-screen flex items-center justify-center">
        <span className="loading loading-spinner loading-lg text-primary"></span>
      </div>
    );

  if (error)
    return (
      <div className="alert alert-error shadow-lg max-w-2xl mx-auto mt-8">
        <span>{error}</span>
      </div>
    );

  return (
    <main className="container mx-auto px-4 py-8">
      {/* Header */}
      <header className="mb-8">
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h1 className="card-title text-2xl mb-4">Patient Dashboard</h1>
            {patientData && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h2 className="text-xl font-semibold">
                    {patientData.fullName}
                  </h2>
                  <p className="text-sm opacity-70">ID: {patientData.id}</p>
                </div>
                <div className="space-y-2">
                  <p>Contact: {patientData.contactNumber}</p>
                  <p>Emergency: {patientData.emergencyContact}</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Medical Records Section */}
      <section className="mb-8">
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h2 className="card-title text-xl mb-4">Medical Records</h2>
            <div className="overflow-x-auto">
              <table className="table table-zebra w-full">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Diagnosis</th>
                    <th>Treatment</th>
                    <th>Prescription</th>
                    <th>Notes</th>
                  </tr>
                </thead>
                <tbody>
                  {medicalRecords.map((record) => (
                    <tr key={record.id}>
                      <td>
                        {new Date(record.recordDate).toLocaleDateString()}
                      </td>
                      <td>{record.diagnosis}</td>
                      <td>{record.treatment}</td>
                      <td>{record.prescription}</td>
                      <td>{record.doctorNotes}</td>
                    </tr>
                  ))}
                  {medicalRecords.length === 0 && (
                    <tr>
                      <td colSpan={5} className="text-center text-gray-500">
                        No medical records found
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      {/* Appointments Section */}
      <section className="mb-8">
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h2 className="card-title text-xl mb-4">Appointments</h2>

            {/* Appointment Booking Form */}
            <form
              onSubmit={handleAppointmentBooking}
              className="form-control gap-4 max-w-md mb-8"
            >
              <h3 className="text-lg font-semibold">
                Schedule New Appointment
              </h3>

              <div>
                <label className="label">
                  <span className="label-text">Appointment Date</span>
                </label>
                <input
                  type="datetime-local"
                  name="date"
                  className="input input-bordered w-full"
                  required
                />
              </div>

              <div>
                <label className="label">
                  <span className="label-text">Select Doctor</span>
                </label>
                <select
                  name="doctorId"
                  className="select select-bordered w-full"
                  required
                >
                  <option value="">Choose a doctor</option>
                  <option value="doc1">Dr. Smith - Cardiology</option>
                  <option value="doc2">Dr. Johnson - General Medicine</option>
                </select>
              </div>

              <div>
                <label className="label">
                  <span className="label-text">Purpose</span>
                </label>
                <input
                  type="text"
                  name="purpose"
                  className="input input-bordered w-full"
                  placeholder="Brief description of the visit"
                  required
                />
              </div>

              <button type="submit" className="btn btn-primary">
                Schedule Appointment
              </button>
            </form>

            {/* Appointments Table */}
            <div className="overflow-x-auto">
              <table className="table table-zebra w-full">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Doctor</th>
                    <th>Purpose</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {appointments.map((appointment) => (
                    <tr key={appointment.id}>
                      <td>
                        {new Date(
                          appointment.appointmentDate
                        ).toLocaleDateString()}
                      </td>
                      <td>{appointment.doctorId}</td>
                      <td>{appointment.purpose}</td>
                      <td>
                        <span
                          className={`badge ${
                            appointment.status === "SCHEDULED"
                              ? "badge-primary"
                              : appointment.status === "COMPLETED"
                                ? "badge-success"
                                : appointment.status === "CANCELLED"
                                  ? "badge-error"
                                  : "badge-warning"
                          }`}
                        >
                          {appointment.status}
                        </span>
                      </td>
                      <td>
                        <button
                          className="btn btn-error btn-sm"
                          onClick={() =>
                            handleAppointmentCancellation(appointment.id)
                          }
                          disabled={appointment.status !== "SCHEDULED"}
                        >
                          Cancel
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      {/* Admission Status Section */}
      <section>
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h2 className="card-title text-xl mb-4">Admission Status</h2>
            {admissionStatus ? (
              <div className="grid gap-4">
                <div className="stats shadow">
                  <div className="stat">
                    <div className="stat-title">Room Number</div>
                    <div className="stat-value">
                      {admissionStatus.bedNumber}
                    </div>
                  </div>
                  <div className="stat">
                    <div className="stat-title">Admission Date</div>
                    <div className="stat-value">
                      {new Date(
                        admissionStatus.admissionDate
                      ).toLocaleDateString()}
                    </div>
                  </div>
                  <div className="stat">
                    <div className="stat-title">Expected Discharge</div>
                    <div className="stat-value">
                      {new Date(
                        admissionStatus.expectedDischargeDate
                      ).toLocaleDateString()}
                    </div>
                  </div>
                </div>

                {admissionStatus.dischargeSummary && (
                  <div className="card bg-base-200">
                    <div className="card-body">
                      <h3 className="card-title">Discharge Summary</h3>
                      <p>{admissionStatus.dischargeSummary}</p>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="alert">
                <span>No active admission</span>
              </div>
            )}
          </div>
        </div>
      </section>
    </main>
  );
}
