import { Schema, model, models } from "mongoose";

const SessionSchema = new Schema(
    {
        session_id: { type: String, required: true, unique: true },
        metadata: {
            customer_id: String,
            loan_amount: Number,
            tenure_months: Number,
            conversation_stage: String,
            customer_data: {
                name: String,
                email: String,
                phone: String,
                city: String,
                pan: String,
                pre_approved_limit: Number,
                credit_score: Number,
            },
        },
        is_active: { type: Boolean, default: true },
    },
    {
        timestamps: { createdAt: "created_at", updatedAt: "updated_at" },
    }
);

export const Session = models.Session || model("Session", SessionSchema);
