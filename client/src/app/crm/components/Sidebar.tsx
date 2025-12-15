"use client";

import { usePathname, useRouter } from "next/navigation";
import { Users, ShieldCheck, CreditCard } from "lucide-react";
import { cn } from "@/lib/utils";

const items = [
  { id: "users", label: "Users", icon: Users },
  { id: "kyc", label: "KYC Details", icon: ShieldCheck },
  { id: "offers", label: "Offers", icon: CreditCard },
];

export default function Sidebar() {
  const router = useRouter();
  const pathname = usePathname();

  const active = pathname.split("/").pop();

  return (
    <div className="p-4">
      <h2 className="text-lg font-semibold text-teal-700 mb-6">
        CRM Dashboard
      </h2>

      <div className="space-y-2">
        {items.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => router.push(`/crm/${id}`)}
            className={cn(
              "w-full flex items-center gap-3 px-4 py-3 rounded-xl transition",
              active === id
                ? "bg-teal-600 text-white shadow"
                : "hover:bg-teal-100 text-teal-700"
            )}
          >
            <Icon className="h-5 w-5" />
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}

