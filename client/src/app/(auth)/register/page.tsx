"use client";

import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { MdOutlineMailOutline } from "react-icons/md";
import { FiLock } from "react-icons/fi";
import { LuUserRound } from "react-icons/lu";
import { toast } from "sonner";
import { redirect } from "next/navigation";
import { register } from "./action";
import { setSessionCookie } from "@/lib/cookie";

const Page = () => {
  const handleRegister = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const name = formData.get("name") as string;
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;
    const confirmPassword = formData.get("confirm-password") as string;

    if (password !== confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }

    const result = await register(name, email, password);
    if (result.error) {
      toast.error(result.error);
      console.log(result.error);
    } else {
      toast.success("Registration successful");
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
            <p className="text-muted-foreground">Create a new account</p>
          </div>

          {/* Desktop header */}
          <div className="hidden lg:block space-y-2">
            <h2 className="text-3xl font-bold text-foreground">Create account</h2>
            <p className="text-muted-foreground">Fill in the details below to get started</p>
          </div>

          {/* Register form */}
          <form className="space-y-6" onSubmit={handleRegister}>
            <div className="space-y-2">
              <Label htmlFor="name" className="text-base">
                Name
              </Label>
              <div className="relative">
                <LuUserRound className="absolute left-4 top-1/2 -translate-y-1/2 size-5 text-muted-foreground" />
                <Input
                  id="name"
                  type="text"
                  name="name"
                  placeholder="Enter your name"
                  required
                  className="h-12 text-base pl-12 pr-4"
                />
              </div>
            </div>

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
              <Label htmlFor="password" className="text-base">
                Password
              </Label>
              <div className="relative">
                <FiLock className="absolute left-4 top-1/2 -translate-y-1/2 size-5 text-muted-foreground" />
                <Input
                  id="password"
                  type="password"
                  name="password"
                  placeholder="Create a password"
                  required
                  className="h-12 text-base pl-12 pr-4"
                  minLength={6}
                  maxLength={12}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="confirm-password" className="text-base">
                Confirm password
              </Label>
              <div className="relative">
                <FiLock className="absolute left-4 top-1/2 -translate-y-1/2 size-5 text-muted-foreground" />
                <Input
                  id="confirm-password"
                  type="password"
                  name="confirm-password"
                  placeholder="Re-enter your password"
                  required
                  className="h-12 text-base pl-12 pr-4"
                  minLength={6}
                  maxLength={12}
                />
              </div>
            </div>

            <Button type="submit" size="lg" className="w-full h-12 text-lg">
              Register
            </Button>

            <div className="text-center">
              <p className="text-sm text-muted-foreground">
                Already have an account?{" "}
                <Link href="/login" className="text-primary font-medium hover:underline">
                  Login here
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
