import { connectDB } from "@/lib/mongodb";
import { Sanction } from "@/models/Sanction";
import SanctionLetterContent from "./SanctionLetterContent";

async function getSanctionData(id: string) {
  try {
    await connectDB();
    const data = await Sanction.findById(id).lean();
    if (!data) return null;
    data._id = data._id?.toString();

    return data;
  } catch (error) {
    console.error("Error fetching sanction data:", error);
    return null;
  }
}

async function getLogo() {
  const imageUrl = "https://cdn.shriramfinance.in/sfl-fe/assets/images/sw-logo.svg";
  const response = await fetch(imageUrl);
  const buffer = Buffer.from(await response.arrayBuffer());
  const base64 = buffer.toString("base64");
  const mimeType = "image/svg+xml";
  return `data:${mimeType};base64,${base64}`;
}

const Page = async ({ params }: { params: Promise<{ id: string }> }) => {
  const { id } = await params;
  const sanction = await getSanctionData(id);

  if (!sanction) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 bg-neutral-100">
        <div className="bg-white p-8 rounded-xl shadow-sm flex flex-col items-center gap-3">
          <p className="text-xl font-bold text-neutral-800">
            Sanction Letter Not Found
          </p>
          <p className="text-neutral-500 text-sm">
            Reference ID: <span className="font-mono">{id}</span>
          </p>
          <div className="h-px w-full bg-neutral-100 my-2" />
          <p className="text-xs text-neutral-400">
            Please contact support if you believe this is an error.
          </p>
        </div>
      </div>
    );
  }

  const logo = await getLogo();

  return <SanctionLetterContent data={sanction} id={id} logo={logo} />;
};

export default Page;
