"use server";

import { Client } from "@/models/Client";
import bcrypt from "bcryptjs";
import { connectDB } from "@/lib/mongodb";

await connectDB();

export const register = async (name: string, email: string, password: string) => {
  try {
    const client = await Client.findOne({ email: email.toLowerCase() });
    if (client) {
      return { error: "Client already exists" };
    }
    const hashedPassword = await bcrypt.hash(password, 10);
    const newClient = await Client.create({
      name: name.trim(),
      email: email.trim().toLowerCase(),
      password: hashedPassword,
    });
    if (!newClient) {
      return { error: "Failed to create client" };
    }
    return { success: true, client: { ...newClient.toObject(), _id: newClient._id.toString() } };
  } catch (error) {
    console.error(error);
    return { error: "Something went wrong" };
  }
};
