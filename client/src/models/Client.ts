import { Schema, model, models } from "mongoose";

const ClientSchema = new Schema(
  {
    name: String,
    email: { type: String, required: true, unique: true },
    phone: { type: String, optional: true, default: null },
    password: String,
  },
  { timestamps: { createdAt: "created_at", updatedAt: "updated_at" } }
);

export const Client = models.Client || model("Client", ClientSchema);
