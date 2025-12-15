"""
Multi-Agent Personal Loan Sales System

Master Agent orchestrates four specialized Worker Agents:
1. Sales Agent - Needs analysis, persuasion, offers, objection handling
2. Verification Agent - KYC, PAN, phone verification
3. Underwriting Agent - Credit score, eligibility, risk assessment
4. Sanction Letter Agent - Generate sanction letter, terms, disbursement info

Requirements:
- Set OPENAI_API_KEY environment variable
- LangChain v1.1.0+
"""

import os
import json
import logging
import uuid
from typing import Optional
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from services import (
    verify_kyc_details, verify_pan, verify_phone, verify_otp,
    fetch_credit_score, get_pre_approved_limit, calculate_emi,
    check_eligibility, verify_salary_slip, generate_sanction_letter,
    get_customer_by_id, get_customer_by_phone, get_customer_by_pan,
    get_interest_rate
)
from session_service import create_session, get_session, update_session
from conversation_service import create_conversation
from models import SessionMetadata

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s',
    # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Model configuration
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
BASE_URL = os.getenv("OPENAI_API_BASE")
TEMPERATURE = 0.1

# Initialize model
model = ChatOpenAI(
    model=MODEL_NAME,
    base_url=BASE_URL if BASE_URL else None,
    temperature=TEMPERATURE,
    max_completion_tokens=1000,
    timeout=30,
)

# Session state to maintain conversation context
session_state = {
    "customer_id": None,
    "loan_amount": None,
    "tenure_months": 60,
    "conversation_stage": "initial",  # initial, needs_analysis, verification, underwriting, sanction
    "customer_data": None,
    "conversation_history": []  # Store full conversation history
}

# Current session ID (None means no active session)
current_session_id: Optional[str] = None


# ==================== SALES AGENT TOOLS ====================

@tool
def analyze_customer_needs(query: str) -> str:
    """
    Analyze customer needs from their query to extract:
    - Desired loan amount
    - Purpose of loan
    - Urgency level
    - Budget constraints
    
    Input: Customer's query or statement about their loan needs
    Returns: JSON string with analyzed needs
    """
    logger.info(f"[TOOL] analyze_customer_needs called with query: {query[:100]}...")
    # This is a simple extraction - in production, this would use NLP/LLM
    analysis = {
        "intent": "loan_inquiry",
        "extracted_info": {
            "loan_amount_mentioned": None,
            "purpose": None,
            "urgency": "normal"
        },
        "message": "Analyzed customer needs from query"
    }
    result = json.dumps(analysis, indent=2)
    logger.info(f"[TOOL] analyze_customer_needs completed")
    return result


@tool
def handle_objection(objection_type: str, context: str = "") -> str:
    """
    Handle common customer objections with persuasive responses.
    
    Common objections:
    - interest_rate: Customer concerned about high interest rates
    - tenure: Customer wants different tenure
    - amount: Customer wants higher/lower amount
    - process: Customer concerned about process complexity
    - existing_loans: Customer has existing EMIs
    
    Input: objection_type (string), optional context
    Returns: Persuasive response addressing the objection
    """
    logger.info(f"[TOOL] handle_objection called - type: {objection_type}, context: {context[:50] if context else 'None'}...")
    responses = {
        "interest_rate": """
        I understand your concern about interest rates. Our rates are competitive and based on your credit profile. 
        For customers with good credit scores, we offer rates starting from 10.5% per annum. 
        Additionally, we have flexible tenure options that can help reduce your EMI burden.
        Would you like me to calculate a personalized EMI for you?
        """,
        "tenure": """
        We offer flexible tenure options from 12 to 60 months. A longer tenure reduces your EMI, 
        while a shorter tenure saves on total interest. Based on your profile, I can suggest the best option.
        What's your preferred EMI range?
        """,
        "amount": """
        I can help you with the right loan amount. We offer loans from ₹50,000 to ₹50,00,000. 
        The amount you're eligible for depends on your credit score, income, and existing obligations.
        Would you like me to check your pre-approved limit?
        """,
        "process": """
        Our process is simple and quick! You can complete everything in this chat:
        1. Quick verification (PAN and phone)
        2. Instant eligibility check
        3. Sanction letter generation
        
        The entire process takes just 10-15 minutes. No lengthy forms or branch visits needed!
        """,
        "existing_loans": """
        Having existing loans doesn't automatically disqualify you. We consider your total debt-to-income ratio.
        If your total EMIs (including the new loan) are within 50% of your income, you're likely eligible.
        Would you like me to check your eligibility?
        """
    }
    
    response = responses.get(objection_type.lower(), 
        "I understand your concern. Let me help you find the best solution. Could you tell me more about what's bothering you?")
    
    result = json.dumps({
        "objection_type": objection_type,
        "response": response.strip(),
        "suggested_next_action": "Continue conversation to address concern"
    }, indent=2)
    logger.info(f"[TOOL] handle_objection completed for type: {objection_type}")
    return result


@tool
def generate_offer(customer_id: Optional[str] = None, loan_amount: Optional[float] = None, 
                   tenure_months: int = 60) -> str:
    """
    Generate a personalized loan offer based on customer profile.
    
    Input: customer_id (optional), loan_amount (optional), tenure_months (default 60)
    Returns: Personalized offer with EMI, interest rate, and benefits
    """
    logger.info(f"[TOOL] generate_offer called - customer_id: {customer_id}, loan_amount: {loan_amount}, tenure: {tenure_months}")
    if customer_id:
        customer = get_customer_by_id(customer_id)
        if customer:
            credit_score = customer["credit_score"]
            pre_approved = customer["pre_approved_limit"]
            salary = customer["salary"]
            
            if not loan_amount:
                loan_amount = min(pre_approved, 500000)  # Default offer
            
            interest_rate = get_interest_rate(credit_score, loan_amount)
            emi_result = calculate_emi(loan_amount, tenure_months, interest_rate)
            
            offer = {
                "customer_id": customer_id,
                "customer_name": customer["name"],
                "loan_amount": loan_amount,
                "tenure_months": tenure_months,
                "interest_rate": interest_rate,
                "emi": emi_result["emi"],
                "pre_approved_limit": pre_approved,
                "credit_score": credit_score,
                "benefits": [
                    "Quick approval process",
                    "Flexible repayment options",
                    "No prepayment charges after 12 months",
                    "Competitive interest rates"
                ],
                "message": f"Based on your profile, we can offer you ₹{loan_amount:,.0f} at {interest_rate}% interest with EMI of ₹{emi_result['emi']:,.0f}"
            }
            result = json.dumps(offer, indent=2)
            logger.info(f"[TOOL] generate_offer completed for customer: {customer_id}")
            return result
    
    # Generic offer if no customer ID
    generic_offer = {
        "loan_amount": loan_amount or 500000,
        "tenure_months": tenure_months,
        "message": "I'd be happy to create a personalized offer for you. Could you share your PAN number so I can check your eligibility?"
    }
    logger.info(f"[TOOL] generate_offer completed (generic offer)")
    return json.dumps(generic_offer, indent=2)


@tool
def detect_intent(user_query: str) -> str:
    """
    Detect user intent from their query.
    Categories: curious, serious, urgent, objection, information_seeking
    
    Input: User's query
    Returns: Intent classification with confidence
    """
    logger.info(f"[TOOL] detect_intent called with query: {user_query[:100]}...")
    query_lower = user_query.lower()
    
    urgent_keywords = ["urgent", "asap", "immediately", "quick", "fast", "today"]
    serious_keywords = ["apply", "interested", "want", "need", "proceed", "how do i"]
    objection_keywords = ["expensive", "high", "rate", "cost", "too much", "better", "cheaper"]
    info_keywords = ["what", "how", "tell me", "explain", "information"]
    
    if any(kw in query_lower for kw in urgent_keywords):
        intent = "urgent"
        confidence = 0.8
    elif any(kw in query_lower for kw in serious_keywords):
        intent = "serious"
        confidence = 0.75
    elif any(kw in query_lower for kw in objection_keywords):
        intent = "objection"
        confidence = 0.7
    elif any(kw in query_lower for kw in info_keywords):
        intent = "information_seeking"
        confidence = 0.7
    else:
        intent = "curious"
        confidence = 0.6
    
    result = json.dumps({
        "intent": intent,
        "confidence": confidence,
        "suggested_action": {
            "urgent": "Fast-track verification and approval",
            "serious": "Provide detailed offer and start application",
            "objection": "Address concern with persuasive response",
            "information_seeking": "Provide clear information",
            "curious": "Engage with benefits and features"
        }.get(intent, "Continue conversation")
    }, indent=2)
    logger.info(f"[TOOL] detect_intent completed - detected intent: {intent} (confidence: {confidence})")
    return result


# ==================== VERIFICATION AGENT TOOLS ====================

@tool
def verify_customer_kyc(name: str, dob: str, address: str, pan: str) -> str:
    """
    Verify customer KYC details (name, DOB, address, PAN).
    
    Input: name, dob (YYYY-MM-DD), address, pan
    Returns: Verification result with customer_id if verified
    """
    logger.info(f"[TOOL] verify_customer_kyc called - name: {name}, pan: {pan}")
    result = verify_kyc_details(name, dob, address, pan)
    if result["verified"]:
        session_state["customer_id"] = result["customer_id"]
        session_state["customer_data"] = result["customer_data"]
        session_state["conversation_stage"] = "verification"
        # Update session in database
        sync_session_to_db()
        logger.info(f"[TOOL] verify_customer_kyc - KYC verified for customer: {result['customer_id']}")
    else:
        logger.warning(f"[TOOL] verify_customer_kyc - KYC verification failed")
    return json.dumps(result, indent=2)


@tool
def verify_customer_pan(pan: str) -> str:
    """
    Verify PAN number format and existence in database.
    
    Input: PAN number (10 characters)
    Returns: Verification result with customer_id if found
    """
    logger.info(f"[TOOL] verify_customer_pan called - PAN: {pan}")
    result = verify_pan(pan)
    if result["verified"]:
        customer = get_customer_by_pan(pan)
        if customer:
            session_state["customer_id"] = result["customer_id"]
            session_state["customer_data"] = customer
            session_state["conversation_stage"] = "verification"
            # Update session in database
            sync_session_to_db()
            logger.info(f"[TOOL] verify_customer_pan - PAN verified for customer: {result['customer_id']}")
    else:
        logger.warning(f"[TOOL] verify_customer_pan - PAN verification failed")
    return json.dumps(result, indent=2)


@tool
def verify_customer_phone(phone: str) -> str:
    """
    Verify phone number and send OTP.
    
    Input: Phone number (with or without country code)
    Returns: OTP sent confirmation (OTP is 123456 for testing)
    """
    logger.info(f"[TOOL] verify_customer_phone called - phone: {phone}")
    result = verify_phone(phone)
    if result["verified"]:
        session_state["customer_id"] = result["customer_id"]
        if not session_state["customer_data"]:
            customer = get_customer_by_phone(phone)
            if customer:
                session_state["customer_data"] = customer
        # Update session in database
        sync_session_to_db()
        logger.info(f"[TOOL] verify_customer_phone - OTP sent to {phone} for customer: {result.get('customer_id')}")
    else:
        logger.warning(f"[TOOL] verify_customer_phone - Phone verification failed")
    return json.dumps(result, indent=2)


@tool
def verify_customer_otp(phone: str, otp: str) -> str:
    """
    Verify OTP sent to phone number.
    
    Input: phone number, otp (6 digits)
    Returns: Verification result
    """
    logger.info(f"[TOOL] verify_customer_otp called - phone: {phone}, OTP: {otp}")
    result = verify_otp(phone, otp)
    if result["verified"]:
        session_state["conversation_stage"] = "underwriting"
        # Update session in database
        sync_session_to_db()
        logger.info(f"[TOOL] verify_customer_otp - OTP verified successfully")
    else:
        logger.warning(f"[TOOL] verify_customer_otp - OTP verification failed")
    return json.dumps(result, indent=2)


# ==================== UNDERWRITING AGENT TOOLS ====================

@tool
def get_customer_credit_score(customer_id: str) -> str:
    """
    Fetch credit score from credit bureau for a customer.
    
    Input: customer_id
    Returns: Credit score (out of 900)
    """
    logger.info(f"[TOOL] get_customer_credit_score called - customer_id: {customer_id}")
    result = fetch_credit_score(customer_id)
    logger.info(f"[TOOL] get_customer_credit_score completed - score: {result.get('credit_score', 'N/A')}")
    return json.dumps(result, indent=2)


@tool
def get_customer_preapproved_limit(customer_id: str) -> str:
    """
    Get pre-approved loan limit from offer mart.
    
    Input: customer_id
    Returns: Pre-approved limit amount
    """
    logger.info(f"[TOOL] get_customer_preapproved_limit called - customer_id: {customer_id}")
    result = get_pre_approved_limit(customer_id)
    logger.info(f"[TOOL] get_customer_preapproved_limit completed - limit: ₹{result.get('pre_approved_limit', 'N/A'):,}" if result.get('pre_approved_limit') else "[TOOL] get_customer_preapproved_limit completed")
    return json.dumps(result, indent=2)


@tool
def check_loan_eligibility(customer_id: str, requested_amount: float, tenure_months: int = 60) -> str:
    """
    Check loan eligibility based on risk rules.
    Returns: approved, conditionally_approved, or rejected with reasons.
    
    Rules:
    - Instant approval if amount <= pre-approved limit
    - Conditional approval if amount <= 2x pre-approved limit (requires salary slip)
    - Rejection if amount > 2x pre-approved limit OR credit score < 700
    
    Input: customer_id, requested_amount, tenure_months (default 60)
    """
    logger.info(f"[TOOL] check_loan_eligibility called - customer_id: {customer_id}, amount: ₹{requested_amount:,.0f}, tenure: {tenure_months} months")
    result = check_eligibility(customer_id, requested_amount, tenure_months)
    if result["eligible"]:
        session_state["loan_amount"] = requested_amount
        session_state["tenure_months"] = tenure_months
        if result["status"] == "approved":
            session_state["conversation_stage"] = "sanction"
            logger.info(f"[TOOL] check_loan_eligibility - Loan APPROVED (instant) for customer: {customer_id}")
        else:
            session_state["conversation_stage"] = "underwriting"
            logger.info(f"[TOOL] check_loan_eligibility - Loan CONDITIONALLY APPROVED for customer: {customer_id}")
        # Update session in database
        sync_session_to_db()
    else:
        logger.warning(f"[TOOL] check_loan_eligibility - Loan REJECTED for customer: {customer_id}, reason: {result.get('reason', 'N/A')}")
    return json.dumps(result, indent=2)


@tool
def calculate_loan_emi(loan_amount: float, tenure_months: int, interest_rate: float) -> str:
    """
    Calculate EMI for given loan parameters.
    
    Input: loan_amount, tenure_months, interest_rate (annual %)
    Returns: EMI calculation details
    """
    logger.info(f"[TOOL] calculate_loan_emi called - amount: ₹{loan_amount:,.0f}, tenure: {tenure_months} months, rate: {interest_rate}%")
    result = calculate_emi(loan_amount, tenure_months, interest_rate)
    if result.get("success"):
        logger.info(f"[TOOL] calculate_loan_emi completed - EMI: ₹{result.get('emi', 'N/A'):,.2f}")
    return json.dumps(result, indent=2)


@tool
def verify_salary_slip_upload(customer_id: str, uploaded: bool = True) -> str:
    """
    Verify uploaded salary slip (simulated - accepts any upload for testing).
    
    Input: customer_id, uploaded (boolean)
    Returns: Verification result
    """
    logger.info(f"[TOOL] verify_salary_slip_upload called - customer_id: {customer_id}, uploaded: {uploaded}")
    result = verify_salary_slip(customer_id, uploaded)
    if result["verified"]:
        logger.info(f"[TOOL] verify_salary_slip_upload - Salary slip verified for customer: {customer_id}")
        # Re-check eligibility after salary slip verification
        if session_state["loan_amount"]:
            eligibility = check_eligibility(
                customer_id, 
                session_state["loan_amount"], 
                session_state["tenure_months"]
            )
            if eligibility["status"] == "approved":
                session_state["conversation_stage"] = "sanction"
                # Update session in database
                sync_session_to_db()
                logger.info(f"[TOOL] verify_salary_slip_upload - Loan approved after salary slip verification")
    else:
        logger.warning(f"[TOOL] verify_salary_slip_upload - Salary slip verification failed")
    return json.dumps(result, indent=2)


# ==================== SANCTION LETTER AGENT TOOLS ====================

@tool
def generate_loan_sanction_letter(customer_id: str, loan_amount: float, 
                                  tenure_months: int, interest_rate: float) -> str:
    """
    Generate sanction letter for approved loan.
    
    Input: customer_id, loan_amount, tenure_months, interest_rate
    Returns: Sanction letter summary with all terms and conditions
    """
    logger.info(f"[TOOL] generate_loan_sanction_letter called - customer_id: {customer_id}, amount: ₹{loan_amount:,.0f}, tenure: {tenure_months} months, rate: {interest_rate}%")
    result = generate_sanction_letter(customer_id, loan_amount, tenure_months, interest_rate)
    if result["success"]:
        session_state["conversation_stage"] = "sanction"
        # Update session in database
        sync_session_to_db()
        logger.info(f"[TOOL] generate_loan_sanction_letter - Sanction letter generated successfully for customer: {customer_id}")
    else:
        logger.error(f"[TOOL] generate_loan_sanction_letter - Failed to generate sanction letter")
    return json.dumps(result, indent=2)


@tool
def get_loan_terms_and_conditions() -> str:
    """
    Get standard loan terms and conditions.
    
    Returns: Terms and conditions text
    """
    logger.info(f"[TOOL] get_loan_terms_and_conditions called")
    terms = {
        "terms": [
            "Loan disbursement within 24-48 hours of document verification",
            "Fixed interest rate for entire tenure",
            "Prepayment allowed after 12 months with minimal charges",
            "Default in payment attracts penalty charges of 2% per month",
            "All disputes subject to jurisdiction of Mumbai courts",
            "Loan can be used for any personal purpose",
            "No collateral required",
            "Processing fee: 2% of loan amount (one-time)"
        ],
        "eligibility_criteria": [
            "Age: 21-60 years",
            "Minimum credit score: 700",
            "Minimum salary: ₹25,000 per month",
            "Indian resident"
        ]
    }
    logger.info(f"[TOOL] get_loan_terms_and_conditions completed")
    return json.dumps(terms, indent=2)


@tool
def get_disbursement_information(customer_id: str) -> str:
    """
    Get disbursement information and next steps.
    
    Input: customer_id
    Returns: Disbursement process details
    """
    logger.info(f"[TOOL] get_disbursement_information called - customer_id: {customer_id}")
    customer = get_customer_by_id(customer_id)
    if customer:
        info = {
            "customer_id": customer_id,
            "customer_name": customer["name"],
            "disbursement_process": [
                "1. Complete KYC verification (if not done)",
                "2. Sign loan agreement",
                "3. Provide bank account details for disbursement",
                "4. Loan amount will be credited within 24-48 hours"
            ],
            "required_documents": [
                "PAN card",
                "Aadhaar card",
                "Salary slip (last 3 months)",
                "Bank statements (last 6 months)"
            ],
            "contact_info": "For assistance, contact our support team at support@tatacapital.com"
        }
        logger.info(f"[TOOL] get_disbursement_information completed for customer: {customer_id}")
        return json.dumps(info, indent=2)
    logger.warning(f"[TOOL] get_disbursement_information - Customer not found: {customer_id}")
    return json.dumps({"error": "Customer not found"}, indent=2)


# ==================== CREATE WORKER AGENTS ====================

# Sales Agent
sales_agent_tools = [
    analyze_customer_needs,
    handle_objection,
    generate_offer,
    detect_intent
]

sales_agent = create_agent(
    model=model,
    tools=sales_agent_tools,
    system_prompt="""You are a Sales Agent for Tata Capital Personal Loans. You're like a friendly, persuasive sales executive who genuinely cares about helping customers.

Your role is to:
1. Understand customer needs naturally through conversation - ask follow-up questions, show interest
2. Handle objections with empathy and solutions - don't just answer, address their concerns
3. Generate personalized offers that excite customers - highlight benefits, not just features
4. Detect customer intent and adapt your tone - be enthusiastic for serious customers, patient for curious ones
5. Focus on conversion - guide customers toward application with gentle persuasion

CONVERSATION STYLE:
- Be conversational and human-like, not robotic
- Use the customer's name when you know it
- Reference previous parts of the conversation to show you're listening
- Ask engaging questions to understand their needs better
- Show enthusiasm about helping them get the loan
- Address concerns with empathy: "I understand your concern about..." then provide solutions
- Use persuasive language: "Great news!", "Perfect!", "I'm excited to help you with..."
- Always try to move the conversation forward naturally toward application

Remember: You're building rapport and trust, just like a human sales executive would."""

)

# Verification Agent
verification_agent_tools = [
    verify_customer_kyc,
    verify_customer_pan,
    verify_customer_phone,
    verify_customer_otp
]

verification_agent = create_agent(
    model=model,
    tools=verification_agent_tools,
    system_prompt="""You are a Verification Agent for Tata Capital Personal Loans. Your role is to:
1. Verify customer KYC details (name, DOB, address, PAN)
2. Verify PAN numbers against database
3. Verify phone numbers and send OTPs
4. Verify OTPs for phone number confirmation

Be thorough and ensure all verification steps are completed before proceeding. Report verification results clearly."""
)

# Underwriting Agent
underwriting_agent_tools = [
    get_customer_credit_score,
    get_customer_preapproved_limit,
    check_loan_eligibility,
    calculate_loan_emi,
    verify_salary_slip_upload
]

underwriting_agent = create_agent(
    model=model,
    tools=underwriting_agent_tools,
    system_prompt="""You are an Underwriting Agent for Tata Capital Personal Loans. Your role is to:
1. Fetch credit scores from credit bureau
2. Get pre-approved loan limits from offer mart
3. Check loan eligibility based on risk rules:
   - Instant approval: loan amount <= pre-approved limit
   - Conditional approval: loan amount <= 2x pre-approved limit (requires salary slip, EMI <= 50% salary)
   - Rejection: loan amount > 2x pre-approved limit OR credit score < 700
4. Calculate EMIs for loan offers
5. Verify salary slips for conditional approvals

Be precise and follow the eligibility rules strictly. Provide clear explanations for approvals, conditional approvals, or rejections."""
)

# Sanction Letter Agent
sanction_agent_tools = [
    generate_loan_sanction_letter,
    get_loan_terms_and_conditions,
    get_disbursement_information
]

sanction_agent = create_agent(
    model=model,
    tools=sanction_agent_tools,
    system_prompt="""You are a Sanction Letter Agent for Tata Capital Personal Loans. Your role is to:
1. Generate sanction letters for approved loans with all details (amount, tenure, EMI, interest rate)
2. Provide terms and conditions
3. Provide disbursement information and next steps

Be clear and comprehensive. Ensure all loan details are accurate in the sanction letter."""
)


# ==================== MASTER AGENT ====================

def get_conversation_summary() -> str:
    """Get a summary of conversation context for worker agents."""
    summary_parts = []
    if session_state.get("customer_id"):
        summary_parts.append(f"Customer ID: {session_state['customer_id']}")
    if session_state.get("loan_amount"):
        summary_parts.append(f"Loan amount discussed: ₹{session_state['loan_amount']:,.0f}")
    if session_state.get("tenure_months"):
        summary_parts.append(f"Tenure discussed: {session_state['tenure_months']} months")
    if session_state.get("conversation_stage"):
        summary_parts.append(f"Current stage: {session_state['conversation_stage']}")
    
    # Get last few messages for context
    if session_state.get("conversation_history"):
        recent_messages = session_state["conversation_history"][-4:]  # Last 4 messages
        context_text = "\n".join([
            f"{'User' if isinstance(msg, HumanMessage) else 'Assistant'}: {msg.content[:100]}"
            for msg in recent_messages if hasattr(msg, 'content')
        ])
        if context_text:
            summary_parts.append(f"Recent conversation:\n{context_text}")
    
    return "\n".join(summary_parts) if summary_parts else "No previous context"


def call_sales_agent(query: str, conversation_context: list = None) -> str:
    """Call Sales Agent to handle sales-related queries."""
    logger.info(f"[AGENT] Sales Agent called with query: {query[:100]}...")
    try:
        # Include conversation context if available
        messages = conversation_context.copy() if conversation_context else []
        
        # Add context summary to help agent remember
        context_summary = get_conversation_summary()
        if context_summary and context_summary != "No previous context":
            enhanced_query = f"[Conversation Context: {context_summary}]\n\nUser's current message: {query}"
        else:
            enhanced_query = query
        
        messages.append(HumanMessage(content=enhanced_query))
        
        result = sales_agent.invoke({"messages": messages})
        if isinstance(result, dict) and "messages" in result:
            response = result["messages"][-1].content
            logger.info(f"[AGENT] Sales Agent completed successfully")
            return response
        elif isinstance(result, list):
            response = result[-1].content if hasattr(result[-1], 'content') else str(result[-1])
            logger.info(f"[AGENT] Sales Agent completed successfully")
            return response
        logger.info(f"[AGENT] Sales Agent completed successfully")
        return str(result)
    except Exception as e:
        logger.error(f"[AGENT] Sales Agent error: {str(e)}")
        return f"Error in Sales Agent: {str(e)}"


def call_verification_agent(query: str, conversation_context: list = None) -> str:
    """Call Verification Agent to handle verification tasks."""
    logger.info(f"[AGENT] Verification Agent called with query: {query[:100]}...")
    try:
        # Include conversation context if available
        messages = conversation_context.copy() if conversation_context else []
        
        # Add context summary
        context_summary = get_conversation_summary()
        if context_summary and context_summary != "No previous context":
            enhanced_query = f"[Conversation Context: {context_summary}]\n\nUser's current message: {query}"
        else:
            enhanced_query = query
        
        messages.append(HumanMessage(content=enhanced_query))
        
        result = verification_agent.invoke({"messages": messages})
        if isinstance(result, dict) and "messages" in result:
            response = result["messages"][-1].content
            logger.info(f"[AGENT] Verification Agent completed successfully")
            return response
        elif isinstance(result, list):
            response = result[-1].content if hasattr(result[-1], 'content') else str(result[-1])
            logger.info(f"[AGENT] Verification Agent completed successfully")
            return response
        logger.info(f"[AGENT] Verification Agent completed successfully")
        return str(result)
    except Exception as e:
        logger.error(f"[AGENT] Verification Agent error: {str(e)}")
        return f"Error in Verification Agent: {str(e)}"


def call_underwriting_agent(query: str, conversation_context: list = None) -> str:
    """Call Underwriting Agent to handle underwriting tasks."""
    logger.info(f"[AGENT] Underwriting Agent called with query: {query[:100]}...")
    try:
        # Include conversation context if available
        messages = conversation_context.copy() if conversation_context else []
        
        # Add context summary
        context_summary = get_conversation_summary()
        if context_summary and context_summary != "No previous context":
            enhanced_query = f"[Conversation Context: {context_summary}]\n\nUser's current message: {query}"
        else:
            enhanced_query = query
        
        messages.append(HumanMessage(content=enhanced_query))
        
        result = underwriting_agent.invoke({"messages": messages})
        if isinstance(result, dict) and "messages" in result:
            response = result["messages"][-1].content
            logger.info(f"[AGENT] Underwriting Agent completed successfully")
            return response
        elif isinstance(result, list):
            response = result[-1].content if hasattr(result[-1], 'content') else str(result[-1])
            logger.info(f"[AGENT] Underwriting Agent completed successfully")
            return response
        logger.info(f"[AGENT] Underwriting Agent completed successfully")
        return str(result)
    except Exception as e:
        logger.error(f"[AGENT] Underwriting Agent error: {str(e)}")
        return f"Error in Underwriting Agent: {str(e)}"


def call_sanction_agent(query: str, conversation_context: list = None) -> str:
    """Call Sanction Letter Agent to handle sanction letter generation."""
    logger.info(f"[AGENT] Sanction Letter Agent called with query: {query[:100]}...")
    try:
        # Include conversation context if available
        messages = conversation_context.copy() if conversation_context else []
        
        # Add context summary
        context_summary = get_conversation_summary()
        if context_summary and context_summary != "No previous context":
            enhanced_query = f"[Conversation Context: {context_summary}]\n\nUser's current message: {query}"
        else:
            enhanced_query = query
        
        messages.append(HumanMessage(content=enhanced_query))
        
        result = sanction_agent.invoke({"messages": messages})
        if isinstance(result, dict) and "messages" in result:
            response = result["messages"][-1].content
            logger.info(f"[AGENT] Sanction Letter Agent completed successfully")
            return response
        elif isinstance(result, list):
            response = result[-1].content if hasattr(result[-1], 'content') else str(result[-1])
            logger.info(f"[AGENT] Sanction Letter Agent completed successfully")
            return response
        logger.info(f"[AGENT] Sanction Letter Agent completed successfully")
        return str(result)
    except Exception as e:
        logger.error(f"[AGENT] Sanction Letter Agent error: {str(e)}")
        return f"Error in Sanction Letter Agent: {str(e)}"


# Master Agent tools (worker agents as tools)
@tool
def route_to_sales_agent(query: str) -> str:
    """Route to Sales Agent for: needs analysis, objection handling, offer generation, intent detection, initial sales conversations."""
    # Pass conversation history to maintain context
    return call_sales_agent(query, session_state.get("conversation_history", []))


@tool
def route_to_verification_agent(query: str) -> str:
    """Route to Verification Agent for: KYC verification, PAN verification, phone verification, OTP verification."""
    # Pass conversation history to maintain context
    return call_verification_agent(query, session_state.get("conversation_history", []))


@tool
def route_to_underwriting_agent(query: str) -> str:
    """Route to Underwriting Agent for: credit score checks, eligibility checks, pre-approved limits, EMI calculations, risk assessment."""
    # Pass conversation history to maintain context
    return call_underwriting_agent(query, session_state.get("conversation_history", []))


@tool
def route_to_sanction_agent(query: str) -> str:
    """Route to Sanction Letter Agent for: generating sanction letters, terms and conditions, disbursement information."""
    # Pass conversation history to maintain context
    return call_sanction_agent(query, session_state.get("conversation_history", []))


master_agent_tools = [
    route_to_sales_agent,
    route_to_verification_agent,
    route_to_underwriting_agent,
    route_to_sanction_agent
]

# Master Agent will be created with dynamic prompt in main()
# We'll create a function to get the system prompt with current state
def get_master_agent_prompt() -> str:
    """Get Master Agent system prompt with current session state."""
    return f"""You are the Master Agent (Orchestrator) for Tata Capital Personal Loans - a sales-focused AI system designed to maximize personal loan conversions.

You're like a smart, persuasive sales executive who guides customers through the complete loan journey from initial interest to sanction letter generation.

CONVERSATION STAGES:
1. Initial/Needs Analysis: Understand customer needs, handle objections, generate offers
2. Verification: Collect and verify KYC details (PAN, phone, address)
3. Underwriting: Check credit score, eligibility, calculate EMIs
4. Sanction: Generate sanction letter with terms and disbursement info

ROUTING LOGIC:
- Sales Agent: Use for initial conversations, understanding needs, handling objections, generating offers, detecting intent. This is your default for most conversations.
- Verification Agent: Use when customer provides PAN, phone number, or KYC details. Also use for OTP verification.
- Underwriting Agent: Use when checking eligibility, credit scores, pre-approved limits, or calculating EMIs. Use after verification is complete.
- Sanction Letter Agent: Use when customer is approved and ready for sanction letter generation.

CRITICAL: MAINTAIN FULL CONVERSATION CONTEXT
- You have access to the ENTIRE conversation history in the messages
- ALWAYS read through previous messages to understand what the customer said earlier
- Reference previous parts of the conversation: "As you mentioned earlier...", "You told me that...", "Based on what you said about..."
- Remember loan amounts, purposes, tenure preferences, and other details from earlier messages
- Don't ask for information the customer already provided - use what they told you before

CONVERSATION STYLE:
- Be conversational, friendly, and persuasive - like a human sales executive
- Show you remember previous conversation: "Great! So you need ₹5 lakhs for home renovation, right?"
- Ask follow-up questions that build on previous answers
- Address concerns with empathy and solutions
- Use natural language, not robotic responses
- Build rapport and trust throughout the conversation

IMPORTANT GUIDELINES:
1. ALWAYS check the conversation history before responding - don't lose context
2. Be sales-oriented and persuasive - focus on conversion, not just answering questions
3. Guide the conversation forward naturally - don't let customers drop off
4. Handle objections persuasively - use Sales Agent for this
5. Complete the full journey - from interest to sanction letter in one conversation
6. Remember details from earlier in the conversation and reference them naturally

Current conversation stage: {session_state["conversation_stage"]}
Current customer ID: {session_state["customer_id"] or "None"}

Always route intelligently based on what the customer is asking and where they are in the loan journey. CRITICALLY: Read the full conversation history in the messages to maintain context."""

# Create master agent (will be recreated with updated prompt when needed)
master_agent = create_agent(
    model=model,
    tools=master_agent_tools,
    system_prompt=get_master_agent_prompt()
)


# ==================== DATABASE INTEGRATION ====================

def sync_session_to_db():
    """Sync session_state to database"""
    if not current_session_id:
        return
    metadata: SessionMetadata = {
        "customer_id": session_state.get("customer_id"),
        "loan_amount": session_state.get("loan_amount"),
        "tenure_months": session_state.get("tenure_months"),
        "conversation_stage": session_state.get("conversation_stage"),
        "customer_data": session_state.get("customer_data")
    }
    update_session(current_session_id, metadata=metadata, conversation_stage=session_state.get("conversation_stage"))


def initialize_session(session_id: Optional[str] = None) -> str:
    """Initialize or resume session"""
    global current_session_id, session_state
    if session_id and (s := get_session(session_id)):
        current_session_id = session_id
        m = s.get("metadata", {})
        session_state.update({k: m.get(k) for k in ["customer_id", "loan_amount", "tenure_months", "conversation_stage", "customer_data"]})
        session_state.setdefault("tenure_months", 60)
        session_state.setdefault("conversation_stage", "initial")
        return session_id
    new_id = session_id or str(uuid.uuid4())
    create_session(new_id, {"conversation_stage": "initial", "tenure_months": 60}, True)
    current_session_id = new_id
    return new_id


# ==================== CLI INTERFACE ====================

def reset_session():
    """Reset session state for new conversation."""
    global session_state, current_session_id
    session_state = {
        "customer_id": None,
        "loan_amount": None,
        "tenure_months": 60,
        "conversation_stage": "initial",
        "customer_data": None,
        "conversation_history": []
    }
    # Create a new session in database
    current_session_id = initialize_session()


def update_master_agent_prompt():
    """Update Master Agent system prompt with current session state."""
    # Note: In LangChain, we'd need to recreate the agent to update the prompt
    # For now, the agent will use tools that have access to session_state
    pass


def main():
    """Interactive CLI for loan sales system."""
    global master_agent
    
    print("=" * 80)
    print("TATA CAPITAL PERSONAL LOANS - AI Sales Assistant")
    print("=" * 80)
    print("\nWelcome! I'm your AI sales assistant. I can help you with:")
    print("  • Understanding your loan needs")
    print("  • Checking eligibility and pre-approved limits")
    print("  • Processing your loan application")
    print("  • Generating sanction letters")
    print("\nType 'exit' or 'quit' to end the conversation.")
    print("Type 'reset' to start a new conversation.")
    print("=" * 80 + "\n")
    
    # Initialize session (creates new session in database)
    reset_session()
    print(f"[New session started: {current_session_id}]\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nThank you for using Tata Capital Personal Loans. Have a great day!")
                break
            
            if user_input.lower() == 'reset':
                reset_session()
                # Recreate master agent with fresh prompt
                master_agent = create_agent(
                    model=model,
                    tools=master_agent_tools,
                    system_prompt=get_master_agent_prompt()
                )
                print("\n[Session reset. Starting fresh conversation.]\n")
                continue
            
            if not current_session_id:
                initialize_session()
            create_conversation(current_session_id, "user", user_input)
            
            # Add user message to conversation history
            user_message = HumanMessage(content=user_input)
            session_state["conversation_history"].append(user_message)
            
            # Recreate master agent with updated prompt to reflect current state
            master_agent = create_agent(
                model=model,
                tools=master_agent_tools,
                system_prompt=get_master_agent_prompt()
            )
            
            print("\n[Processing...]")
            logger.info(f"[AGENT] Master Agent called - User input: {user_input[:100]}...")
            logger.info(f"[AGENT] Master Agent - Conversation history length: {len(session_state['conversation_history'])} messages")
            logger.info(f"[AGENT] Master Agent - Session ID: {current_session_id}")
            
            # Invoke master agent with FULL conversation history
            result = master_agent.invoke({"messages": session_state["conversation_history"]})
            
            # Extract response - find the last AI message (skip tool calls)
            response = None
            if isinstance(result, dict) and "messages" in result:
                # Find the last AIMessage (not tool calls or other message types)
                for msg in reversed(result["messages"]):
                    if isinstance(msg, AIMessage) or (hasattr(msg, 'content') and hasattr(msg, 'type') and msg.type == 'ai'):
                        if hasattr(msg, 'content') and msg.content:
                            response = msg.content
                            break
                
                # Fallback: get last message with content
                if not response:
                    for msg in reversed(result["messages"]):
                        if hasattr(msg, 'content') and msg.content:
                            response = msg.content
                            break
                            
            elif isinstance(result, list):
                # If result is a list, find the last AI message
                for msg in reversed(result):
                    if isinstance(msg, AIMessage) or (hasattr(msg, 'content') and hasattr(msg, 'type') and getattr(msg, 'type', None) == 'ai'):
                        if hasattr(msg, 'content') and msg.content:
                            response = msg.content
                            break
                
                # Fallback
                if not response and result:
                    last_msg = result[-1]
                    if hasattr(last_msg, 'content'):
                        response = last_msg.content
                    else:
                        response = str(last_msg)
            
            # Final fallback
            if not response:
                response = str(result)
            
            create_conversation(current_session_id, "assistant", response, "master")
            
            # Add assistant response to history
            if response:
                session_state["conversation_history"].append(AIMessage(content=response))
                logger.info(f"[AGENT] Master Agent completed - Response length: {len(response)} characters")
            
            # Sync session state to database
            sync_session_to_db()
            
            print(f"\nAssistant: {response}\n")
            print(f"[Session ID: {current_session_id}]\n")
            print("-" * 80 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nThank you for using Tata Capital Personal Loans. Have a great day!")
            break
        except Exception as e:
            print(f"\n[Error: {str(e)}]\n")
            print("Please try again or type 'exit' to quit.\n")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
