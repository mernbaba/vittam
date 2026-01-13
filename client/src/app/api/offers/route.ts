import { NextResponse } from "next/server";
import { connectDB } from "@/lib/mongodb";
import { OfferTemplate } from "@/models/OfferTemplate";

export async function GET() {
  await connectDB();

  const offers = await OfferTemplate.find({}).select({}).lean();

  return NextResponse.json({ success: true, offers });
}
