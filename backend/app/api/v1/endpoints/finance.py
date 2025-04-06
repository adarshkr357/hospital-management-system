from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel
from ....core.security import get_current_user, check_permissions
from ....utils.db_utils import execute_query
from ....utils.date_utils import validate_date_range
from ....sql.queries.finance_queries import *

router = APIRouter()

class FinancialOverviewOut(BaseModel):
    daily_revenue: float
    monthly_revenue: float
    outstanding_amount: float

class FinancialReportOut(BaseModel):
    id: int
    date: date
    department_id: int
    amount: float
    type: str
    source: str

# Financial overview query
GET_FINANCIAL_OVERVIEW_QUERY = """
    SELECT 
        (SELECT COALESCE(SUM(amount), 0) FROM revenue WHERE date = CURRENT_DATE AND type = 'DAILY') AS daily_revenue,
        (SELECT COALESCE(SUM(amount), 0) FROM revenue WHERE date_trunc('month', date) = date_trunc('month', CURRENT_DATE) AND type = 'MONTHLY') AS monthly_revenue,
        (SELECT COALESCE(SUM(amount), 0) FROM bills WHERE status IN ('PENDING', 'OVERDUE')) AS outstanding_amount
    ;
"""

@router.get("/bills")
async def get_all_bills(
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: dict = Depends(check_permissions(["ADMIN", "FINANCE"])),
):
    """Get all bills with optional filters"""
    try:
        query = GET_ALL_BILLS_QUERY
        params = []

        if status:
            query = query.replace("ORDER BY", f"WHERE b.status = %s ORDER BY")
            params.append(status)

        if start_date and end_date:
            if not validate_date_range(start_date, end_date):
                raise HTTPException(status_code=400, detail="Invalid date range")
            query = query.replace(
                "ORDER BY", f"WHERE b.generated_date BETWEEN %s AND %s ORDER BY"
            )
            params.extend([start_date, end_date])

        bills = execute_query(query, tuple(params), fetch_all=True)
        return bills
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/overview", response_model=FinancialOverviewOut)
def get_financial_overview(current_user: dict = Depends(get_current_user)):
    """
    Get an overview of financial metrics including daily and monthly revenue, as well as outstanding amounts.
    """
    report = execute_query(GET_FINANCIAL_OVERVIEW_QUERY, fetch_one=True)
    if not report:
        raise HTTPException(status_code=404, detail="Financial overview not available")
    return report

@router.post("/bills")
async def create_bill(
    bill_data: dict,
    current_user: dict = Depends(check_permissions(["ADMIN", "FINANCE"])),
):
    """Create new bill"""
    try:
        result = execute_query(
            CREATE_BILL_QUERY,
            (
                bill_data["patient_id"],
                bill_data.get("admission_id"),
                bill_data["amount"],
                bill_data["due_date"],
            ),
            fetch_one=True,
        )

        # Send notification to patient
        # TODO: Implement notification system

        return {"message": "Bill created successfully", "bill_id": result["id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/bills/{bill_id}/status")
async def update_bill_status(
    bill_id: int,
    status: str,
    payment_method: Optional[str] = None,
    current_user: dict = Depends(check_permissions(["ADMIN", "FINANCE"])),
):
    """Update bill status"""
    try:
        execute_query(UPDATE_BILL_STATUS_QUERY, (status, payment_method, bill_id))
        return {"message": "Bill status updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/revenue/report")
async def get_revenue_report(
    current_user: dict = Depends(check_permissions(["ADMIN", "FINANCE"]))
):
    """Get revenue report"""
    try:
        report = execute_query(GET_REVENUE_REPORT_QUERY, fetch_one=True)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insurance-claims")
async def get_insurance_claims(
    status: Optional[str] = None,
    current_user: dict = Depends(check_permissions(["ADMIN", "FINANCE"])),
):
    """Get all insurance claims"""
    try:
        query = GET_INSURANCE_CLAIMS_QUERY
        params = []

        if status:
            query = query.replace("ORDER BY", f"WHERE ic.status = %s ORDER BY")
            params.append(status)

        claims = execute_query(query, tuple(params), fetch_all=True)
        return claims
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/insurance-claims")
async def create_insurance_claim(
    claim_data: dict,
    current_user: dict = Depends(check_permissions(["ADMIN", "FINANCE"])),
):
    """Create new insurance claim"""
    try:
        result = execute_query(
            CREATE_INSURANCE_CLAIM_QUERY,
            (
                claim_data["patient_id"],
                claim_data["bill_id"],
                claim_data["insurance_provider"],
                claim_data["claim_amount"],
            ),
            fetch_one=True,
        )
        return {
            "message": "Insurance claim created successfully",
            "claim_id": result["id"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reports", response_model=List[FinancialReportOut])
def get_financial_reports(current_user: dict = Depends(get_current_user)):
    """
    Return a list of financial reports.
    """
    reports = execute_query(GET_FINANCE_REPORTS_QUERY, fetch_all=True)
    if reports is None:
        raise HTTPException(status_code=404, detail="No financial reports available")
    return reports