import { NextResponse } from "next/server";
import { connectDB } from "@/lib/mongodb";
import { Sanction } from "@/models/Sanction";
import { User } from "@/models/User";
import { Kyc } from "@/models/Kyc";
import { Session } from "../../../../models/Session";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    await connectDB();

    // Parallel fetch for better performance
    const todayStart = new Date();
    todayStart.setHours(0, 0, 0, 0);
    const todayEnd = new Date();
    todayEnd.setHours(23, 59, 59, 999);

    const [
      totalRevenueResult,
      activeCustomersCount,
      activeSessionsCount,
      applicationsCount,
      monthlyData,
      recentSessions,
      todaysLeadsCount,
      todaysEngagedLeadsCount,
      todaysDeadLeadsCount,
    ] = await Promise.all([
      // 1. Total Revenue (Sum of Sanctioned User loan amounts)
      Sanction.aggregate([{ $group: { _id: null, total: { $sum: "$loan_amount" } } }]),

      // 2. Active Customers (Total Users)
      User.countDocuments({}),

      // 3. Active Sessions (Total Active Sessions)
      Session.countDocuments({ is_active: true }),

      // 4. Applications (Total KYC records)
      Kyc.countDocuments({}),

      // 5. Monthly Chart Data (Aggregation by month)
      Sanction.aggregate([
        {
          $group: {
            _id: { $month: "$created_at" },
            total: { $sum: "$loan_amount" },
          },
        },
        { $sort: { _id: 1 } },
      ]),

      // 6. Recent Sessions (Latest 5)
      Session.find({
        is_active: true,
        "metadata.customer_id": { $exists: true, $ne: null },
      })
        .sort({ created_at: -1 })
        .limit(5)
        .lean(),

      // 7. Today's Leads (all sessions created today)
      Session.countDocuments({
        created_at: { $gte: todayStart, $lte: todayEnd },
      }),

      // 8. Today's Engaged Leads (customer_id present)
      Session.countDocuments({
        created_at: { $gte: todayStart, $lte: todayEnd },
        "metadata.customer_id": { $exists: true, $ne: null },
      }),

      // 9. Today's Dead Leads (customer_id missing)
      Session.countDocuments({
        created_at: { $gte: todayStart, $lte: todayEnd },
        $or: [{ "metadata.customer_id": { $exists: false } }, { "metadata.customer_id": null }],
      }),
    ]);

    // Format Monthly Data
    const months = ["Jan", "Feb", "Mar", "Apr", "May"];
    const chartData = months.map((name, index) => {
      const monthData = monthlyData.find((d) => d._id === index + 1);
      return {
        name,
        total: monthData ? monthData.total : 0,
      };
    });

    // Format Recent Activity from Session Metadata
    const formattedRecentActivity = recentSessions.map((session: any) => ({
      user: {
        name: session.metadata?.customer_data?.name || "Anonymous",
        email: session.metadata?.customer_data?.email || "No Email",
        image: null,
      },
      createdAt: session.created_at,
    }));

    return NextResponse.json({
      success: true,
      stats: {
        revenue: totalRevenueResult[0]?.total || 0,
        customers: activeCustomersCount,
        sessions: activeSessionsCount,
        applications: applicationsCount,
        todaysLeads: todaysLeadsCount,
        todaysEngagedLeads: todaysEngagedLeadsCount,
        todaysDeadLeads: todaysDeadLeadsCount,
      },
      chartData,
      recentActivity: formattedRecentActivity,
    });
  } catch (err) {
    console.error("Dashboard Stats Error:", err);
    return NextResponse.json(
      { success: false, error: "Failed to fetch dashboard stats" },
      { status: 500 }
    );
  }
}
