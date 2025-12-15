import { NextResponse } from "next/server";
import clientPromise from "@/lib/mongodb";

export async function GET() {
  try {
    const client = await clientPromise;
    const db = client.db("Vittam"); 

    const users = await db
      .collection("users")
      .find({})
      .project({
        name: 1,
        dob: 1,
        city: 1,
        phone:1,
        email:1,
        current_loans: 1,
        credit_score: 1,
        pre_approved_limit: 1,
        _id: 0,
      })
      .toArray();

    return NextResponse.json({ success: true, users });
  } catch (error) {
    return NextResponse.json(
      { success: false, message: "Failed to fetch users" },
      { status: 500 }
    );
  }
}
