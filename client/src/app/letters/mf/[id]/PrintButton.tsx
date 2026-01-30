"use client";

import { Button } from "@/components/ui/button";

const PrintButton = ({ children }: { children: React.ReactNode }) => {
  const handlePrint = () => {
    window.print();
  };

  return <Button onClick={handlePrint}>{children}</Button>;
};

export default PrintButton;
