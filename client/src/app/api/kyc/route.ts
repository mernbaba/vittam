import { NextResponse } from "next/server";
import clientPromise from "@/lib/mongodb";

export async function GET() {
  try {
    const client = await clientPromise;
    const db = client.db("Vittam"); 

    const kyc = await db
      .collection("kyc")
      .find({})
      .project({
        _id: 0,
        name: 1,
        pan: 1,
        credit_score: 1,
        phone:1,
        address:1,
        dob:1,
        verified: 1,
      })
      .toArray();

    return NextResponse.json({ success: true, kyc });
  } catch (error) {
    return NextResponse.json(
      { success: false, message: "Failed to fetch KYC details" },
      { status: 500 }
    );
  }
}
