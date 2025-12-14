"""
Hardcoded Data Services for Personal Loan Sales System

This module provides mock services for:
- Customer data (CRM)
- Credit bureau scores
- KYC verification
- PAN verification
- Phone verification
- Offer mart (pre-approved limits)
- EMI calculations
- Risk rules and eligibility
"""

import logging
from typing import Dict, Optional
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)


# Synthetic Customer Database (Minimum 10 customers)
CUSTOMER_DATABASE = {
    "CUST001": {
        "name": "Rajesh Kumar",
        "age": 32,
        "city": "Mumbai",
        "phone": "+919876543210",
        "email": "rajesh.kumar@email.com",
        "pan": "ABCDE1234F",
        "address": "123, MG Road, Mumbai - 400001",
        "dob": "1992-05-15",
        "salary": 75000,
        "current_loans": [{"type": "Home Loan", "emi": 25000, "outstanding": 5000000}],
        "credit_score": 780,
        "pre_approved_limit": 500000,
        "existing_customer": True
    },
    "CUST002": {
        "name": "Priya Sharma",
        "age": 28,
        "city": "Delhi",
        "phone": "+919876543211",
        "email": "priya.sharma@email.com",
        "pan": "FGHIJ5678K",
        "address": "456, Connaught Place, Delhi - 110001",
        "dob": "1996-08-22",
        "salary": 60000,
        "current_loans": [],
        "credit_score": 720,
        "pre_approved_limit": 300000,
        "existing_customer": False
    },
    "CUST003": {
        "name": "Amit Patel",
        "age": 35,
        "city": "Ahmedabad",
        "phone": "+919876543212",
        "email": "amit.patel@email.com",
        "pan": "KLMNO9012P",
        "address": "789, CG Road, Ahmedabad - 380009",
        "dob": "1989-03-10",
        "salary": 95000,
        "current_loans": [{"type": "Car Loan", "emi": 15000, "outstanding": 800000}],
        "credit_score": 810,
        "pre_approved_limit": 800000,
        "existing_customer": True
    },
    "CUST004": {
        "name": "Sneha Reddy",
        "age": 29,
        "city": "Bangalore",
        "phone": "+919876543213",
        "email": "sneha.reddy@email.com",
        "pan": "PQRST3456U",
        "address": "321, Brigade Road, Bangalore - 560001",
        "dob": "1995-11-05",
        "salary": 55000,
        "current_loans": [],
        "credit_score": 690,
        "pre_approved_limit": 200000,
        "existing_customer": False
    },
    "CUST005": {
        "name": "Vikram Singh",
        "age": 42,
        "city": "Pune",
        "phone": "+919876543214",
        "email": "vikram.singh@email.com",
        "pan": "UVWXY7890Z",
        "address": "654, FC Road, Pune - 411004",
        "dob": "1982-07-18",
        "salary": 120000,
        "current_loans": [{"type": "Personal Loan", "emi": 20000, "outstanding": 600000}],
        "credit_score": 750,
        "pre_approved_limit": 1000000,
        "existing_customer": True
    },
    "CUST006": {
        "name": "Anjali Mehta",
        "age": 26,
        "city": "Chennai",
        "phone": "+919876543215",
        "email": "anjali.mehta@email.com",
        "pan": "ZABCD1234E",
        "address": "987, Mount Road, Chennai - 600002",
        "dob": "1998-01-25",
        "salary": 48000,
        "current_loans": [],
        "credit_score": 680,
        "pre_approved_limit": 150000,
        "existing_customer": False
    },
    "CUST007": {
        "name": "Rohit Verma",
        "age": 38,
        "city": "Kolkata",
        "phone": "+919876543216",
        "email": "rohit.verma@email.com",
        "pan": "EFGHI5678J",
        "address": "147, Park Street, Kolkata - 700016",
        "dob": "1986-09-12",
        "salary": 88000,
        "current_loans": [{"type": "Home Loan", "emi": 30000, "outstanding": 7000000}],
        "credit_score": 790,
        "pre_approved_limit": 600000,
        "existing_customer": True
    },
    "CUST008": {
        "name": "Kavita Nair",
        "age": 31,
        "city": "Hyderabad",
        "phone": "+919876543217",
        "email": "kavita.nair@email.com",
        "pan": "JKLMN9012O",
        "address": "258, Banjara Hills, Hyderabad - 500034",
        "dob": "1993-04-30",
        "salary": 70000,
        "current_loans": [],
        "credit_score": 740,
        "pre_approved_limit": 400000,
        "existing_customer": False
    },
    "CUST009": {
        "name": "Manish Gupta",
        "age": 45,
        "city": "Jaipur",
        "phone": "+919876543218",
        "email": "manish.gupta@email.com",
        "pan": "OPQRS3456T",
        "address": "369, MI Road, Jaipur - 302001",
        "dob": "1979-12-08",
        "salary": 110000,
        "current_loans": [{"type": "Car Loan", "emi": 18000, "outstanding": 900000}],
        "credit_score": 820,
        "pre_approved_limit": 1200000,
        "existing_customer": True
    },
    "CUST010": {
        "name": "Divya Iyer",
        "age": 27,
        "city": "Coimbatore",
        "phone": "+919876543219",
        "email": "divya.iyer@email.com",
        "pan": "TUVWX7890Y",
        "address": "741, DB Road, Coimbatore - 641018",
        "dob": "1997-06-14",
        "salary": 52000,
        "current_loans": [],
        "credit_score": 710,
        "pre_approved_limit": 250000,
        "existing_customer": False
    },
    "CUST011": {
        "name": "Suresh Menon",
        "age": 33,
        "city": "Kochi",
        "phone": "+919876543220",
        "email": "suresh.menon@email.com",
        "pan": "YZABC1234D",
        "address": "852, MG Road, Kochi - 682016",
        "dob": "1991-10-20",
        "salary": 65000,
        "current_loans": [],
        "credit_score": 730,
        "pre_approved_limit": 350000,
        "existing_customer": False
    },
    "CUST012": {
        "name": "Pooja Desai",
        "age": 30,
        "city": "Surat",
        "phone": "+919876543221",
        "email": "pooja.desai@email.com",
        "pan": "DEFGH5678I",
        "address": "963, Ring Road, Surat - 395002",
        "dob": "1994-02-28",
        "salary": 58000,
        "current_loans": [],
        "credit_score": 705,
        "pre_approved_limit": 280000,
        "existing_customer": False
    }
}

# Valid PAN numbers mapping
VALID_PANS = {customer["pan"]: customer_id for customer_id, customer in CUSTOMER_DATABASE.items()}

# Valid Phone numbers mapping
VALID_PHONES = {customer["phone"]: customer_id for customer_id, customer in CUSTOMER_DATABASE.items()}

# Interest rates based on credit score and loan amount
INTEREST_RATES = {
    "excellent": {"min": 10.5, "max": 12.0},  # 750+
    "good": {"min": 12.5, "max": 14.5},      # 700-749
    "fair": {"min": 15.0, "max": 18.0},      # 650-699
    "poor": {"min": 18.5, "max": 24.0}       # <650
}


def get_customer_by_phone(phone: str) -> Optional[Dict]:
    """Get customer data from CRM by phone number."""
    logger.info(f"[SERVICE] get_customer_by_phone called - phone: {phone}")
    customer_id = VALID_PHONES.get(phone)
    if customer_id:
        logger.info(f"[SERVICE] get_customer_by_phone - Customer found: {customer_id}")
        return {"customer_id": customer_id, **CUSTOMER_DATABASE[customer_id]}
    logger.warning(f"[SERVICE] get_customer_by_phone - Customer not found for phone: {phone}")
    return None


def get_customer_by_pan(pan: str) -> Optional[Dict]:
    """Get customer data from CRM by PAN number."""
    logger.info(f"[SERVICE] get_customer_by_pan called - PAN: {pan}")
    customer_id = VALID_PANS.get(pan.upper())
    if customer_id:
        logger.info(f"[SERVICE] get_customer_by_pan - Customer found: {customer_id}")
        return {"customer_id": customer_id, **CUSTOMER_DATABASE[customer_id]}
    logger.warning(f"[SERVICE] get_customer_by_pan - Customer not found for PAN: {pan}")
    return None


def get_customer_by_id(customer_id: str) -> Optional[Dict]:
    """Get customer data by customer ID."""
    logger.info(f"[SERVICE] get_customer_by_id called - customer_id: {customer_id}")
    if customer_id in CUSTOMER_DATABASE:
        logger.info(f"[SERVICE] get_customer_by_id - Customer found: {customer_id}")
        return {"customer_id": customer_id, **CUSTOMER_DATABASE[customer_id]}
    logger.warning(f"[SERVICE] get_customer_by_id - Customer not found: {customer_id}")
    return None


def verify_kyc_details(name: str, dob: str, address: str, pan: str) -> Dict:
    """Verify KYC details against customer database."""
    logger.info(f"[SERVICE] verify_kyc_details called - name: {name}, pan: {pan}")
    pan_upper = pan.upper()
    customer = get_customer_by_pan(pan_upper)
    
    if not customer:
        return {
            "verified": False,
            "message": "PAN not found in our records",
            "customer_id": None
        }
    
    # Check if details match
    matches = []
    if customer["name"].lower() == name.lower():
        matches.append("name")
    if customer["dob"] == dob:
        matches.append("dob")
    if customer["address"].lower() == address.lower():
        matches.append("address")
    
    if len(matches) >= 2:  # At least 2 fields should match
        logger.info(f"[SERVICE] verify_kyc_details - KYC verified. Matched fields: {', '.join(matches)}")
        return {
            "verified": True,
            "message": f"KYC verified. Matched fields: {', '.join(matches)}",
            "customer_id": customer["customer_id"],
            "customer_data": customer
        }
    else:
        logger.warning(f"[SERVICE] verify_kyc_details - KYC verification failed. Only {len(matches)} field(s) matched")
        return {
            "verified": False,
            "message": f"KYC verification failed. Only {len(matches)} field(s) matched: {', '.join(matches) if matches else 'none'}",
            "customer_id": customer["customer_id"]
        }


def verify_pan(pan: str) -> Dict:
    """Verify PAN number format and existence."""
    logger.info(f"[SERVICE] verify_pan called - PAN: {pan}")
    pan_upper = pan.upper().strip()
    
    # Basic PAN format validation (5 letters, 4 digits, 1 letter)
    if len(pan_upper) != 10:
        return {
            "verified": False,
            "message": "Invalid PAN format. PAN should be 10 characters long.",
            "customer_id": None
        }
    
    if not (pan_upper[:5].isalpha() and pan_upper[5:9].isdigit() and pan_upper[9].isalpha()):
        return {
            "verified": False,
            "message": "Invalid PAN format. Format should be: 5 letters, 4 digits, 1 letter.",
            "customer_id": None
        }
    
    customer = get_customer_by_pan(pan_upper)
    if customer:
        logger.info(f"[SERVICE] verify_pan - PAN verified successfully for customer: {customer['customer_id']}")
        return {
            "verified": True,
            "message": "PAN verified successfully",
            "customer_id": customer["customer_id"],
            "customer_name": customer["name"]
        }
    else:
        logger.warning(f"[SERVICE] verify_pan - PAN not found in database")
        return {
            "verified": False,
            "message": "PAN not found in our database",
            "customer_id": None
        }


def verify_phone(phone: str) -> Dict:
    """Verify phone number and send OTP (simulated)."""
    logger.info(f"[SERVICE] verify_phone called - phone: {phone}")
    phone_clean = phone.strip()
    
    # Basic phone validation
    if not phone_clean.startswith("+91") and not phone_clean.startswith("91"):
        phone_clean = "+91" + phone_clean.lstrip("+")
    
    customer = get_customer_by_phone(phone_clean)
    if customer:
        # Simulate OTP generation
        otp = "123456"  # In real system, this would be randomly generated
        logger.info(f"[SERVICE] verify_phone - OTP sent to {phone_clean} for customer: {customer['customer_id']}")
        return {
            "verified": True,
            "message": f"OTP sent to {phone_clean}. OTP: {otp} (for testing)",
            "customer_id": customer["customer_id"],
            "customer_name": customer["name"],
            "otp": otp
        }
    else:
        logger.warning(f"[SERVICE] verify_phone - Phone number not found in database")
        return {
            "verified": False,
            "message": f"Phone number {phone_clean} not found in our database",
            "customer_id": None
        }


def verify_otp(phone: str, otp: str) -> Dict:
    """Verify OTP (simulated - accepts any 6-digit OTP for testing)."""
    logger.info(f"[SERVICE] verify_otp called - phone: {phone}, OTP: {otp}")
    if len(otp) == 6 and otp.isdigit():
        customer = get_customer_by_phone(phone)
        if customer:
            logger.info(f"[SERVICE] verify_otp - OTP verified successfully for customer: {customer['customer_id']}")
            return {
                "verified": True,
                "message": "Phone number verified successfully",
                "customer_id": customer["customer_id"]
            }
    logger.warning(f"[SERVICE] verify_otp - Invalid OTP")
    return {
        "verified": False,
        "message": "Invalid OTP"
    }


def fetch_credit_score(customer_id: str) -> Dict:
    """Fetch credit score from mock credit bureau API."""
    logger.info(f"[SERVICE] fetch_credit_score called - customer_id: {customer_id}")
    customer = get_customer_by_id(customer_id)
    if customer:
        score = customer["credit_score"]
        logger.info(f"[SERVICE] fetch_credit_score - Credit score retrieved: {score}/900 for customer: {customer_id}")
        return {
            "success": True,
            "customer_id": customer_id,
            "credit_score": score,
            "max_score": 900,
            "message": f"Credit score retrieved: {score}/900"
        }
    logger.warning(f"[SERVICE] fetch_credit_score - Customer not found: {customer_id}")
    return {
        "success": False,
        "message": "Customer not found",
        "credit_score": None
    }


def get_pre_approved_limit(customer_id: str) -> Dict:
    """Get pre-approved loan limit from offer mart."""
    logger.info(f"[SERVICE] get_pre_approved_limit called - customer_id: {customer_id}")
    customer = get_customer_by_id(customer_id)
    if customer:
        limit = customer["pre_approved_limit"]
        logger.info(f"[SERVICE] get_pre_approved_limit - Pre-approved limit: ₹{limit:,} for customer: {customer_id}")
        return {
            "success": True,
            "customer_id": customer_id,
            "pre_approved_limit": limit,
            "message": f"Pre-approved limit: ₹{limit:,}"
        }
    logger.warning(f"[SERVICE] get_pre_approved_limit - Customer not found: {customer_id}")
    return {
        "success": False,
        "message": "Customer not found",
        "pre_approved_limit": None
    }


def calculate_emi(loan_amount: float, tenure_months: int, interest_rate: float) -> Dict:
    """Calculate EMI (Equated Monthly Installment)."""
    logger.info(f"[SERVICE] calculate_emi called - amount: ₹{loan_amount:,.0f}, tenure: {tenure_months} months, rate: {interest_rate}%")
    if loan_amount <= 0 or tenure_months <= 0 or interest_rate <= 0:
        logger.warning(f"[SERVICE] calculate_emi - Invalid input parameters")
        return {
            "success": False,
            "message": "Invalid input parameters"
        }
    
    monthly_rate = interest_rate / (12 * 100)
    emi = loan_amount * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
    total_amount = emi * tenure_months
    total_interest = total_amount - loan_amount
    
    logger.info(f"[SERVICE] calculate_emi - Calculated EMI: ₹{round(emi, 2):,.2f}, Total: ₹{round(total_amount, 2):,.2f}")
    return {
        "success": True,
        "loan_amount": loan_amount,
        "tenure_months": tenure_months,
        "interest_rate": interest_rate,
        "emi": round(emi, 2),
        "total_amount": round(total_amount, 2),
        "total_interest": round(total_interest, 2)
    }


def get_interest_rate(credit_score: int, loan_amount: float) -> float:
    """Get interest rate based on credit score and loan amount."""
    logger.info(f"[SERVICE] get_interest_rate called - credit_score: {credit_score}, loan_amount: ₹{loan_amount:,.0f}")
    if credit_score >= 750:
        category = "excellent"
    elif credit_score >= 700:
        category = "good"
    elif credit_score >= 650:
        category = "fair"
    else:
        category = "poor"
    
    rate_range = INTEREST_RATES[category]
    # Higher loan amounts get slightly better rates
    if loan_amount >= 1000000:
        rate = rate_range["min"]
    elif loan_amount >= 500000:
        rate = (rate_range["min"] + rate_range["max"]) / 2
    else:
        rate = rate_range["max"]
    
    rate = round(rate, 2)
    logger.info(f"[SERVICE] get_interest_rate - Calculated rate: {rate}% (category: {category})")
    return rate


def check_eligibility(customer_id: str, requested_amount: float, tenure_months: int = 60) -> Dict:
    """
    Check loan eligibility based on risk rules.
    
    Rules:
    1. Instant Approval: If requested_amount <= pre_approved_limit
    2. Conditional Approval: If requested_amount <= 2 * pre_approved_limit (requires salary slip)
    3. Rejection: If requested_amount > 2 * pre_approved_limit OR credit_score < 700
    """
    logger.info(f"[SERVICE] check_eligibility called - customer_id: {customer_id}, amount: ₹{requested_amount:,.0f}, tenure: {tenure_months} months")
    customer = get_customer_by_id(customer_id)
    if not customer:
        logger.warning(f"[SERVICE] check_eligibility - Customer not found: {customer_id}")
        return {
            "eligible": False,
            "status": "rejected",
            "message": "Customer not found",
            "reason": "Customer ID invalid"
        }
    
    credit_score = customer["credit_score"]
    pre_approved_limit = customer["pre_approved_limit"]
    salary = customer["salary"]
    
    # Rule 1: Rejection if credit score < 700
    if credit_score < 700:
        logger.warning(f"[SERVICE] check_eligibility - REJECTED: Credit score {credit_score} < 700")
        return {
            "eligible": False,
            "status": "rejected",
            "message": "Loan application rejected",
            "reason": f"Credit score {credit_score} is below minimum requirement of 700",
            "credit_score": credit_score,
            "pre_approved_limit": pre_approved_limit
        }
    
    # Rule 2: Rejection if requested amount > 2 * pre_approved_limit
    if requested_amount > 2 * pre_approved_limit:
        logger.warning(f"[SERVICE] check_eligibility - REJECTED: Amount ₹{requested_amount:,} > 2x limit ₹{2 * pre_approved_limit:,}")
        return {
            "eligible": False,
            "status": "rejected",
            "message": "Loan application rejected",
            "reason": f"Requested amount ₹{requested_amount:,} exceeds maximum eligible limit of ₹{2 * pre_approved_limit:,}",
            "requested_amount": requested_amount,
            "pre_approved_limit": pre_approved_limit,
            "max_eligible": 2 * pre_approved_limit
        }
    
    # Rule 3: Instant Approval if requested_amount <= pre_approved_limit
    if requested_amount <= pre_approved_limit:
        interest_rate = get_interest_rate(credit_score, requested_amount)
        emi_result = calculate_emi(requested_amount, tenure_months, interest_rate)
        
        logger.info(f"[SERVICE] check_eligibility - INSTANT APPROVAL: Amount ₹{requested_amount:,} <= limit ₹{pre_approved_limit:,}")
        return {
            "eligible": True,
            "status": "approved",
            "message": "Loan approved instantly",
            "requested_amount": requested_amount,
            "pre_approved_limit": pre_approved_limit,
            "credit_score": credit_score,
            "interest_rate": interest_rate,
            "tenure_months": tenure_months,
            "emi": emi_result["emi"],
            "approval_type": "instant"
        }
    
    # Rule 4: Conditional Approval (requires salary slip)
    # Check if EMI <= 50% of salary
    interest_rate = get_interest_rate(credit_score, requested_amount)
    emi_result = calculate_emi(requested_amount, tenure_months, interest_rate)
    emi = emi_result["emi"]
    max_allowable_emi = salary * 0.5
    
    if emi <= max_allowable_emi:
        logger.info(f"[SERVICE] check_eligibility - CONDITIONAL APPROVAL: EMI ₹{emi:,.2f} <= 50% salary (₹{max_allowable_emi:,.2f})")
        return {
            "eligible": True,
            "status": "conditionally_approved",
            "message": "Loan conditionally approved - salary slip verification required",
            "requested_amount": requested_amount,
            "pre_approved_limit": pre_approved_limit,
            "credit_score": credit_score,
            "interest_rate": interest_rate,
            "tenure_months": tenure_months,
            "emi": emi,
            "salary": salary,
            "max_allowable_emi": max_allowable_emi,
            "approval_type": "conditional",
            "requires_salary_slip": True
        }
    else:
        logger.warning(f"[SERVICE] check_eligibility - REJECTED: EMI ₹{emi:,.2f} > 50% salary (₹{max_allowable_emi:,.2f})")
        return {
            "eligible": False,
            "status": "rejected",
            "message": "Loan application rejected",
            "reason": f"EMI ₹{emi:,.2f} exceeds 50% of salary (₹{max_allowable_emi:,.2f})",
            "requested_amount": requested_amount,
            "emi": emi,
            "salary": salary,
            "max_allowable_emi": max_allowable_emi
        }


def verify_salary_slip(customer_id: str, salary_slip_uploaded: bool = True) -> Dict:
    """Simulate salary slip verification (accepts any upload for testing)."""
    logger.info(f"[SERVICE] verify_salary_slip called - customer_id: {customer_id}, uploaded: {salary_slip_uploaded}")
    customer = get_customer_by_id(customer_id)
    if not customer:
        logger.warning(f"[SERVICE] verify_salary_slip - Customer not found: {customer_id}")
        return {
            "verified": False,
            "message": "Customer not found"
        }
    
    if salary_slip_uploaded:
        logger.info(f"[SERVICE] verify_salary_slip - Salary slip verified successfully for customer: {customer_id}")
        return {
            "verified": True,
            "message": "Salary slip verified successfully",
            "customer_id": customer_id,
            "verified_salary": customer["salary"]
        }
    logger.warning(f"[SERVICE] verify_salary_slip - Salary slip not uploaded")
    return {
        "verified": False,
        "message": "Salary slip not uploaded"
    }


def generate_sanction_letter(customer_id: str, loan_amount: float, tenure_months: int, interest_rate: float) -> Dict:
    """Generate sanction letter summary (text format for now)."""
    logger.info(f"[SERVICE] generate_sanction_letter called - customer_id: {customer_id}, amount: ₹{loan_amount:,.0f}, tenure: {tenure_months} months, rate: {interest_rate}%")
    customer = get_customer_by_id(customer_id)
    if not customer:
        logger.error(f"[SERVICE] generate_sanction_letter - Customer not found: {customer_id}")
        return {
            "success": False,
            "message": "Customer not found"
        }
    
    emi_result = calculate_emi(loan_amount, tenure_months, interest_rate)
    
    sanction_letter = {
        "success": True,
        "customer_id": customer_id,
        "customer_name": customer["name"],
        "sanction_date": datetime.now().strftime("%Y-%m-%d"),
        "loan_amount": loan_amount,
        "tenure_months": tenure_months,
        "interest_rate": interest_rate,
        "emi": emi_result["emi"],
        "total_amount": emi_result["total_amount"],
        "disbursement_account": "To be provided by customer",
        "terms_and_conditions": [
            "Loan amount will be disbursed within 24-48 hours of document verification",
            "Interest rate is fixed for the entire tenure",
            "Prepayment charges apply as per policy",
            "Default in payment will attract penalty charges",
            "All disputes subject to jurisdiction of Mumbai courts"
        ],
        "summary": f"""
SANCTION LETTER

Dear {customer["name"]},

We are pleased to inform you that your Personal Loan application has been approved.

Loan Details:
- Sanctioned Amount: ₹{loan_amount:,.2f}
- Tenure: {tenure_months} months ({tenure_months//12} years {tenure_months%12} months)
- Interest Rate: {interest_rate}% per annum
- EMI: ₹{emi_result["emi"]:,.2f}
- Total Amount Payable: ₹{emi_result["total_amount"]:,.2f}

This sanction is valid for 30 days from the date of issue.

Please contact us to complete the disbursement process.

Best Regards,
Tata Capital Personal Loans Team
        """.strip()
    }
    
    logger.info(f"[SERVICE] generate_sanction_letter - Sanction letter generated successfully for customer: {customer_id}")
    return sanction_letter
