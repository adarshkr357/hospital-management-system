// types/index.ts

// User Base Type
export interface User {
    id: string;
    email: string;
    password: string;
    role: 'ADMIN' | 'PATIENT' | 'STAFF' | 'FINANCE';
    createdAt: Date;
}

// Patient Related Types
export interface Patient {
    id: string;
    userId: string;
    fullName: string;
    contactNumber: string;
    emergencyContact: string;
    bloodGroup: string;
    allergies: string[];
    currentMedications: string[];
}

export interface MedicalRecord {
    id: string;
    patientId: string;
    diagnosis: string;
    treatment: string;
    prescription: string;
    testResults: string;
    doctorNotes: string;
    recordDate: Date;
}

export interface Appointment {
    id: string;
    patientId: string;
    doctorId: string;
    appointmentDate: Date;
    status: 'SCHEDULED' | 'COMPLETED' | 'CANCELLED' | 'NO_SHOW';
    purpose: string;
    reminderSent: boolean;
    createdAt: Date;
}

export interface Admission {
    id: string;
    patientId: string;
    bedNumber: string;
    admissionDate: Date;
    expectedDischargeDate: Date;
    actualDischargeDate?: Date;
    status: 'ADMITTED' | 'DISCHARGED';
    dischargeSummary?: string;
}

// Staff Related Types
export interface Department {
    id: string;
    name: string;
    headStaffId: string;
    currentWorkload: number;
    requiredStaff: number;
    createdAt: Date;
}

export interface Staff {
    id: string;
    userId: string;
    departmentId: string;
    fullName: string;
    role: 'DOCTOR' | 'NURSE' | 'ADMIN_STAFF';
    specialization?: string;
    contactNumber: string;
}

export interface StaffSchedule {
    id: string;
    staffId: string;
    shiftStart: Date;
    shiftEnd: Date;
    workDays: WeekDay[];
    isOvertime: boolean;
}

export type WeekDay = 'MON' | 'TUE' | 'WED' | 'THU' | 'FRI' | 'SAT' | 'SUN';

export interface Attendance {
    id: string;
    staffId: string;
    date: Date;
    clockIn?: Date;
    clockOut?: Date;
    status: 'PRESENT' | 'ABSENT' | 'LEAVE' | 'HALF_DAY';
    overtimeHours: number;
}

export interface Leave {
    id: string;
    staffId: string;
    startDate: Date;
    endDate: Date;
    leaveType: string;
    status: 'PENDING' | 'APPROVED' | 'REJECTED';
    reason: string;
}

// Finance Related Types
export interface Bill {
    id: string;
    patientId: string;
    admissionId?: string;
    amount: number;
    generatedDate: Date;
    dueDate: Date;
    status: 'PAID' | 'PENDING' | 'OVERDUE';
    paymentMethod?: string;
}

export interface InsuranceClaim {
    id: string;
    patientId: string;
    billId: string;
    insuranceProvider: string;
    claimAmount: number;
    submissionDate: Date;
    status: 'SUBMITTED' | 'APPROVED' | 'REJECTED' | 'PENDING';
    rejectionReason?: string;
    settlementDate?: Date;
}

export interface Revenue {
    id: string;
    date: Date;
    departmentId: string;
    amount: number;
    type: 'DAILY' | 'MONTHLY';
    source: string;
}

export interface RevenueData {
    dailyRevenue: number;
    monthlyRevenue: number;
    outstandingAmount: number;
    revenueByDepartment: {
        departmentId: string;
        amount: number;
    }[];
    revenueHistory: {
        date: Date;
        amount: number;
    }[];
}

// Notification Types
export interface Notification {
    id: string;
    userId: string;
    type: 'APPOINTMENT' | 'BILL' | 'SHIFT_CHANGE' | 'LEAVE_STATUS' | 'OVERTIME';
    message: string;
    createdAt: Date;
    read: boolean;
}
