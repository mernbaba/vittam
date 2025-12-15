import { NextResponse } from "next/server";
import { connectDB } from "@/lib/mongodb";
import { OfferTemplate } from "@/models/OfferTemplate";

export async function GET() {
  await connectDB();

  const offers = await OfferTemplate.find({ active: true })
    .select(
      "name min_credit_score max_credit_score min_amount max_amount min_tenure_months max_tenure_months base_rate processing_fee_pct active"
    )
    .lean();

  return NextResponse.json({ success: true, offers });
}
