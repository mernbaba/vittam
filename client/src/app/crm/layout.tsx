import Sidebar from "./components/Sidebar";

export default function CRMLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex bg-[#FFF8F1]">
      <aside className="w-64 bg-[#FDF6EE] border-r">
        <Sidebar />
      </aside>
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}

