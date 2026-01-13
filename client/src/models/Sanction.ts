import { Schema, model, models } from "mongoose";

const BankDetailsSchema = new Schema(
  {
    account_number: String,
    ifsc_code: String,
    account_holder_name: String,
    bank_name: String,
  },
  { _id: false }
);

const SanctionSchema = new Schema(
  {
    customer_id: String,
    session_id: String,
    customer_name: String,
    loan_amount: Number,
    tenure_months: Number,
    interest_rate: Number,
    emi: Number,
    total_amount: Number,
    total_interest: Number,
    processing_fee: Number,
    processing_fee_pct: Number,
    bank_details: BankDetailsSchema,
    validity_days: { type: Number, default: 30 },
    status: { type: String, default: "active" },
  },
  {
    timestamps: { createdAt: "created_at", updatedAt: "updated_at" },
  }
);

export const Sanction = models.Sanction || model("Sanction", SanctionSchema);
