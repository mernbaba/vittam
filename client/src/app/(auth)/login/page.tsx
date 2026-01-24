"use client";

import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { MdOutlineMailOutline } from "react-icons/md";
import { FiLock } from "react-icons/fi";
import { toast } from "sonner";
import { login } from "./action";
import { redirect } from "next/navigation";
import { setSessionCookie } from "@/lib/cookie";

const Page = () => {
  const handleLogin = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;
    const result = await login(email, password);
    if (result.error) {
      toast.error(result.error);
      console.log(result.error);
    } else {
      toast.success("Login successful");
      await setSessionCookie({
        id: result.client._id.toString(),
        email: result.client.email,
        name: result.client.name,
      });
      redirect("/dashboard");
    }
  };

  return (
    <div className="min-h-screen flex bg-white">
      <div className="hidden lg:flex lg:w-1/2 bg-teal-900"></div>

      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-md space-y-8">
          {/* Mobile header */}
          <div className="lg:hidden text-center space-y-2 mb-8">
            <h1 className="text-3xl font-bold text-foreground">Vittam</h1>
            <p className="text-muted-foreground">Sign in to your account</p>
          </div>

          {/* Desktop header */}
          <div className="hidden lg:block space-y-2">
            <h2 className="text-3xl font-bold text-foreground">Sign in</h2>
            <p className="text-muted-foreground">Enter your credentials to access your account</p>
          </div>

          {/* Login form */}
          <form className="space-y-6" onSubmit={handleLogin}>
            <div className="space-y-2">
              <Label htmlFor="email" className="text-base">
                Email
              </Label>
              <div className="relative">
                <MdOutlineMailOutline className="absolute left-4 top-1/2 -translate-y-1/2 size-5 text-muted-foreground" />
                <Input
                  id="email"
                  type="email"
                  name="email"
                  placeholder="Enter your email"
                  required
                  className="h-12 text-base pl-12 pr-4"
                />
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="password" className="text-base">
                  Password
                </Label>
                <Link
                  href="/forgot-password"
                  className="text-sm text-primary hover:underline"
                  prefetch={false}
                >
                  Forgot password?
                </Link>
              </div>
              <div className="relative">
                <FiLock className="absolute left-4 top-1/2 -translate-y-1/2 size-5 text-muted-foreground" />
                <Input
                  id="password"
                  type="password"
                  name="password"
                  placeholder="Enter your password"
                  required
                  className="h-12 text-base pl-12 pr-4"
                  maxLength={12}
                />
              </div>
            </div>

            <Button type="submit" size="lg" className="w-full h-12 text-lg">
              Sign in
            </Button>

            <div className="text-center">
              <p className="text-sm text-muted-foreground">
                Don&apos;t have an account?{" "}
                <Link href="/register" className="text-primary font-medium hover:underline">
                  Register here
                </Link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Page;
