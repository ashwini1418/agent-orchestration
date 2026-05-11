// FRONTEND_AGENT | 2026-05-10 | Registration page
import { Link } from "react-router-dom";
import { RegisterForm } from "@/components/auth/RegisterForm";

export function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-sm bg-white rounded-xl shadow-lg p-8">
        <div className="text-center mb-8">
          <div className="text-4xl mb-2">🤖</div>
          <h1 className="text-2xl font-bold text-gray-900">Create Account</h1>
          <p className="text-sm text-gray-500 mt-1">Get started with the Orchestrator</p>
        </div>
        <RegisterForm />
        <p className="text-center text-sm text-gray-500 mt-6">
          Already have an account?{" "}
          <Link to="/login" className="text-blue-600 hover:underline font-medium">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
