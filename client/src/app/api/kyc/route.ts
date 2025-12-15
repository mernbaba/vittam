import { NextResponse } from "next/server";
import { connectDB } from "@/lib/mongodb";
import { Kyc } from "@/models/Kyc";

export async function GET() {
  await connectDB();

  const kyc = await Kyc.find({})
    .select("name pan credit_score phone address dob")
    .lean();

  return NextResponse.json({ success: true, kyc });
}
