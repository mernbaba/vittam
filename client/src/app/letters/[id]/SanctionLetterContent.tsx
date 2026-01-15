"use client";

import { jsPDF } from "jspdf";
import html2canvas from "html2canvas-pro";
import {
  HiOutlineArrowDownTray,
  HiOutlinePrinter,
  HiOutlineShieldCheck,
} from "react-icons/hi2";
import PrintButton from "./PrintButton";
import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export interface SanctionData {
  customer_id: string;
  customer_name: string;
  loan_amount: number;
  tenure_months: number;
  interest_rate: number;
  emi: number;
  total_amount: number;
  processing_fee: number;
  created_at: Date;
  validity_days: number;
  bank_details?: {
    account_number?: string;
    ifsc_code?: string;
    account_holder_name?: string;
  };
}

const SanctionLetterContent = ({
  data,
  id,
  logo,
}: {
  data: SanctionData;
  id: string;
  logo: string;
}) => {
  const sanctionDateString = new Date(data.created_at).toLocaleDateString(
    "en-IN",
    {
      day: "2-digit",
      month: "long",
      year: "numeric",
    }
  );

  const validUntilDate = new Date(data.created_at);
  validUntilDate.setDate(validUntilDate.getDate() + (data.validity_days || 30));
  const validUntilString = validUntilDate.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });

  const handleDownloadPDF = async () => {
    if (typeof window === "undefined") return;

    const element = document.querySelector(".sanction-letter") as HTMLElement;
    if (!element) return;

    // Hide elements not for PDF
    // const toHide: HTMLElement[] = [];
    // element.querySelectorAll(".print-hidden").forEach((el) => {
    //   if (el instanceof HTMLElement) {
    //     toHide.push(el);
    //     el.style.display = "none";
    //   }
    // });

    const canvas = await html2canvas(element, {
      scale: 3,
      useCORS: true,
      backgroundColor: "#fff",
      logging: true,
      allowTaint: false,
    });
    const imgData = canvas.toDataURL("image/jpeg", 0.98);

    const pdf = new jsPDF({
      unit: "mm",
      format: "a4",
      orientation: "portrait",
    });

    // Calculate width and height to fit A4
    const a4Width = 210;
    const a4Height = 297;
    const imgProps = {
      width: canvas.width,
      height: canvas.height,
    };
    const pdfWidth = a4Width;
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

    // Fill page with white to prevent black lines when the image is smaller than page
    // pdf.setFillColor(255, 255, 255);
    // pdf.rect(0, 0, a4Width, a4Height, "F");

    pdf.addImage(
      imgData,
      "JPEG",
      0,
      0,
      pdfWidth,
      pdfHeight > a4Height ? a4Height : pdfHeight
    );

    pdf.save(`sanction-letter-${id}.pdf`);

    // Restore hidden elements
    // toHide.forEach((el) => {
    //   el.style.display = "";
    // });
  };

  return (
    <div className="min-h-screen bg-neutral-100 p-4 md:p-8 flex flex-col items-center text-black font-sans sanction-letter-container">
      <div className="w-full max-w-[800px] flex justify-between items-center mb-6 print-hidden">
        <h1 className="text-lg font-bold">Sanction Letter</h1>
        <div className="flex gap-2">
          <PrintButton>
            <HiOutlinePrinter className="w-4 h-4" />
            Print Letter
          </PrintButton>
          <Button onClick={handleDownloadPDF}>
            <HiOutlineArrowDownTray className="size-4" />
            Download PDF
          </Button>
        </div>
      </div>

      <div className="w-full max-w-[800px] bg-white shadow-2xl print-shadow-none print-full-width flex flex-col sanction-letter">
        <div className="bg-[#1961AC] print-exact-blue text-white print-exact-white p-6 md:p-7 mb-3">
          <div className="flex justify-between items-start">
            <div className="space-y-3">
              <Image
                width={800}
                height={100}
                src={logo}
                alt="Tata Capital Logo"
                className="h-8 w-auto object-contain brightness-0 invert print-logo-invert"
              />
              <div className="text-xs text-blue-50 print-exact-blue-text font-sans leading-tight opacity-95">
                <p>11th Floor, Tower A, Peninsula Business Park,</p>
                <p>Ganpatrao Kadam Marg, Lower Parel, Mumbai - 400013</p>
              </div>
            </div>
            <div className="text-right font-sans text-[11px] leading-tight space-y-1.5 pt-1">
              <p className="font-bold text-sm uppercase tracking-wider">
                LOAN SANCTION LETTER
              </p>
              <p className="text-blue-100 print-exact-blue-text font-semibold uppercase">
                REF: SL-{id}
              </p>
              <p className="text-blue-100 print-exact-blue-text font-semibold">
                DATE: {sanctionDateString}
              </p>
            </div>
          </div>
        </div>

        <div className="flex-1 space-y-4 text-[12px] leading-snug px-10 md:px-12 py-4 min-h-[80dvh] print:min-h-[75dvh]">
          <div className="space-y-1">
            <p className="font-bold">To,</p>
            <p className="font-bold uppercase text-base">
              {data.customer_name}
            </p>
            <p>Customer ID: {data.customer_id}</p>
          </div>

          <div className="text-center">
            <p className="font-bold underline uppercase py-2">
              Sub: Sanction of Personal Loan Facilitated by Tata Capital
            </p>
          </div>

          <p>
            Dear {data.customer_name},<br />
            <br />
            With reference to your application for a personal loan, we are
            pleased to inform you that your request has been approved in
            principle. The sanction of the loan is subject to the following key
            terms and conditions:
          </p>

          {/* Key Terms Table */}
          <table className="w-full border-collapse border border-black shadow-sm">
            <thead>
              <tr className="bg-neutral-50 text-[11px]">
                <th className="border border-black p-3 text-left w-1/2 uppercase tracking-tight">
                  Parameters
                </th>
                <th className="border border-black p-3 text-left uppercase tracking-tight">
                  Sanctioned Terms
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-black p-3 font-bold">
                  Loan Sanctioned Amount
                </td>
                <td className="border border-black p-3 font-bold">
                  INR {data.loan_amount.toLocaleString("en-IN")} /-
                </td>
              </tr>
              <tr>
                <td className="border border-black p-3 font-bold">
                  Loan Tenure (Months)
                </td>
                <td className="border border-black p-3">
                  {data.tenure_months} Months
                </td>
              </tr>
              <tr>
                <td className="border border-black p-3 font-bold">
                  Annual Interest Rate (%)
                </td>
                <td className="border border-black p-3">
                  {data.interest_rate}% P.A. (Fixed)
                </td>
              </tr>
              <tr>
                <td className="border border-black p-3 font-bold">
                  Equated Monthly Installment (EMI)
                </td>
                <td className="border border-black p-3 font-bold">
                  INR {data.emi.toLocaleString("en-IN")} /-
                </td>
              </tr>
              <tr>
                <td className="border border-black p-3 font-bold">
                  Processing Fee (Incl. GST)
                </td>
                <td className="border border-black p-3">
                  INR {data.processing_fee.toLocaleString("en-IN")} /-
                </td>
              </tr>
              <tr>
                <td className="border border-black p-3 font-bold">
                  Total Amount Payable Over Tenure
                </td>
                <td className="border border-black p-3 font-bold">
                  INR {data.total_amount.toLocaleString("en-IN")} /-
                </td>
              </tr>
            </tbody>
          </table>

          {/* Disbursement Info */}
          <div className="space-y-2">
            <p className="font-bold uppercase text-[11px] border-b border-black pb-1 inline-block">
              Validity & Disbursement:
            </p>
            <div className="text-[13px]">
              <p>
                This offer is valid until{" "}
                <span className="font-bold">{validUntilString}</span>.
              </p>
              <p>
                The sanctioned amount will be disbursed to the following bank
                account after digital verification:
              </p>
              <div className="ml-3 my-1 text-[12px] leading-6">
                <div className="flex items-center gap-2">
                  <span className="font-semibold">Account Holder Name:</span>
                  <span className="font-mono">
                    {data.bank_details?.account_holder_name || "XXXXXXXXXX"}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-semibold">Account Number:</span>{" "}
                  <span className="font-mono">
                    {data.bank_details?.account_number || "XXXXXXXXXX"}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-semibold">IFSC Code:</span>{" "}
                  <span className="font-mono uppercase">
                    {data.bank_details?.ifsc_code || "XXXXXXXXXXX"}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Charges and Conditions */}
          <div className="grid grid-cols-2 gap-12">
            <div className="space-y-2">
              <p className="font-bold uppercase text-[11px] border-b border-black pb-1 inline-block">
                Charges Description:
              </p>
              <ul className="text-[11px] space-y-1 font-medium">
                <li>• Penal Interest: 3% p.m. on defaulted amount</li>
                <li>• Cheque/ECS Dishonour: INR 600 per instance</li>
                <li>• Mandate Rejection: INR 450 per instance</li>
                <li>• Foreclosure: Allowed after 12 months</li>
              </ul>
            </div>
            <div className="space-y-2">
              <p className="font-bold uppercase text-[11px] border-b border-black pb-1 inline-block">
                Standard Terms:
              </p>
              <ul className="text-[11px] space-y-1 font-medium">
                <li>• Recovery via NACH/Auto-debit mandate</li>
                <li>• Fixed Rate for complete loan tenure</li>
                <li>• Digital Signature required for agreement</li>
                <li>• No collateral or security required</li>
              </ul>
            </div>
          </div>

          <div className="flex items-center justify-between gap-4 mt-20">
            <div className="flex-1">
              <p className="text-xs italic leading-tight">
                <span className="font-bold">Note:</span> This is an
                electronically generated document. No physical signature is
                required. For any assistance, please contact us at{" "}
                <Link
                  href="mailto:support@tatacapital.com"
                  className="font-bold underline"
                >
                  support@tatacapital.com
                </Link>{" "}
                or call our helpline at{" "}
                <Link href="tel:18602676060" className="font-bold underline">
                  1860-267-6060
                </Link>
                . Powered by{" "}
                <Link href="/" className="font-bold underline">
                  Vittam AI
                </Link>
                .
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-600 border border-emerald-100 bg-emerald-50 px-3 py-1 rounded-sm flex-shrink-0">
              <HiOutlineShieldCheck className="size-4" />
              VERIFIED ELECTRONICALLY
            </div>
          </div>
        </div>

        <div className="px-10 pb-2 pt-1 flex flex-col items-center border-t border-neutral-50">
          <p className="text-[9px] text-gray-400 font-sans tracking-widest uppercase">
            © {new Date().getFullYear()} TATA CAPITAL FINANCIAL SERVICES LIMITED
          </p>
        </div>
      </div>
    </div>
  );
};

export default SanctionLetterContent;
