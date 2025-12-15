import { NextResponse } from "next/server";
import clientPromise from "@/lib/mongodb";

export async function GET() {
  try {
    const client = await clientPromise;
    const db = client.db("Vittam");

    const offers = await db
      .collection("offer_template")
      .find({ active: true })
      .project({
        _id: 0,
        name: 1,
        min_credit_score: 1,
        max_credit_score: 1,
        min_amount: 1,
        max_amount: 1,
        min_tenure_months: 1,
        max_tenure_months: 1,
        base_rate: 1,
        processing_fee_pct: 1,
      })
      .toArray();

    return NextResponse.json({ success: true, offers });
  } catch (error) {
    return NextResponse.json(
      { success: false, message: "Failed to fetch offers" },
      { status: 500 }
    );
  }
}
