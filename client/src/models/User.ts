import { Schema, model, models } from "mongoose";

const CurrentLoanSchema = new Schema(
  {
    type: String,
    emi: Number,
    outstanding: Number,
  },
  { _id: false }
);

const UserSchema = new Schema(
  {
    name: String,
    dob: Date,
    city: String,
    phone: {
      type: String,
      match: /^[0-9]{10}$/,
    },
    email: String,
    current_loans: [CurrentLoanSchema],
    pre_approved_limit: Number,
  },
  { timestamps: true }
);

export const User = models.User || model("User", UserSchema);
