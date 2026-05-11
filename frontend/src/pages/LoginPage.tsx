// FRONTEND_AGENT | 2026-05-10 | Login page
import { Link } from "react-router-dom";
import { LoginForm } from "@/components/auth/LoginForm";

export function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-sm bg-white rounded-xl shadow-lg p-8">
        <div className="text-center mb-8">
          <div className="text-4xl mb-2">🤖</div>
          <h1 className="text-2xl font-bold text-gray-900">Multiagent Orchestrator</h1>
          <p className="text-sm text-gray-500 mt-1">Sign in to your account</p>
        </div>
        <LoginForm />
        <p className="text-center text-sm text-gray-500 mt-6">
          Don't have an account?{" "}
          <Link to="/register" className="text-blue-600 hover:underline font-medium">
            Register
          </Link>
        </p>
      </div>
    </div>
  );
}
