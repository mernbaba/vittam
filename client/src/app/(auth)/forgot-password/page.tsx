import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { MdOutlineMailOutline } from "react-icons/md";

const Page = () => {
  return (
    <div className="min-h-screen flex bg-white">
      <div className="hidden lg:flex lg:w-1/2 bg-teal-900"></div>

      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-md space-y-8">
          {/* Mobile header */}
          <div className="lg:hidden text-center space-y-2 mb-8">
            <h1 className="text-3xl font-bold text-foreground">Vittam</h1>
            <p className="text-muted-foreground">Forgot your password?</p>
          </div>

          {/* Desktop header */}
          <div className="hidden lg:block space-y-2">
            <h2 className="text-3xl font-bold text-foreground">Forgot your password?</h2>
            <p className="text-muted-foreground">Enter your email to reset your password</p>
          </div>

          {/* Forgot password form */}
          <form className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="email" className="text-base">
                Enter your email
              </Label>
              <div className="relative">
                <MdOutlineMailOutline className="absolute left-4 top-1/2 -translate-y-1/2 size-5 text-muted-foreground" />
                <Input
                  id="email"
                  type="email"
                  placeholder="Enter your email to reset your password"
                  required
                  className="h-12 text-base pl-12 pr-4"
                />
              </div>
            </div>

            <Button type="submit" size="lg" className="w-full h-12 text-lg">
              Reset password
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
