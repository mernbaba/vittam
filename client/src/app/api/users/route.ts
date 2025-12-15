import { NextResponse } from "next/server";
import { connectDB } from "@/lib/mongodb";
import { User } from "@/models/User";

export async function GET() {
  await connectDB();

  const users = await User.find({})
    .select("name dob city phone email current_loans pre_approved_limit")
    .lean();

  return NextResponse.json({ success: true, users });
}
