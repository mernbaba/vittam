import { connectDB } from "@/lib/mongodb";
import { Sanction } from "@/models/Sanction";
import SanctionsPanel from "./SanctionsPanel";

async function getSanctions() {
    await connectDB();
    const sanctions = await Sanction.find({})
        .sort({ created_at: -1 })
        .lean();

    // Transform _id to string for client component
    return JSON.parse(JSON.stringify(sanctions));
}

export default async function Page() {
    const sanctionsData = await getSanctions();

    return <SanctionsPanel sanctionsData={sanctionsData} />;
}
