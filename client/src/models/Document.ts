import { Schema, model, models } from "mongoose";

const DocumentSchema = new Schema({
  _id: { type: String, required: true },
  doc_id: { type: String, required: true },
  session_id: { type: String, required: true },
  doc_name: { type: String, required: true },
  file_path: { type: String, required: true },
  file_size: { type: Number, required: true },
  original_filename: { type: String, required: true },
  uploaded_at: { type: Date, required: true },
});

export const Document = models.Document || model("Document", DocumentSchema);
