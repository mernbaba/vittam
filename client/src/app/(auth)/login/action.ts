"use server";

import { Client } from "@/models/Client";
import bcrypt from "bcryptjs";
import { connectDB } from "@/lib/mongodb";

await connectDB();

export const login = async (email: string, password: string) => {
  try {
    const client = await Client.findOne({ email: email.toLowerCase() });
    if (!client) {
      return { error: "Client not found" };
    }
    if (!(await bcrypt.compare(password, client.password))) {
      return { error: "Invalid password" };
    }
    return { success: true, client: { ...client.toObject(), _id: client._id.toString() } };
  } catch (error) {
    console.error(error);
    return { error: "Something went wrong" };
  }
};
