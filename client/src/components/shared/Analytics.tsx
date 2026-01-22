"use client";

import { useEffect } from "react";
import Clarity from "@microsoft/clarity";

const Analytics = () => {
  useEffect(() => {
    if (!process.env.NEXT_PUBLIC_CLARITY_ID) {
      return;
    }
    Clarity.init(process.env.NEXT_PUBLIC_CLARITY_ID);
  }, []);

  return null;
};

export default Analytics;
