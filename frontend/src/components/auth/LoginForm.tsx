// FRONTEND_AGENT | 2026-05-10 | Login form with validation
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useAuth } from "@/hooks/useAuth";
import { Button } from "@/components/common/Button";
import { ApiError } from "@/api/client";

const schema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(1, "Password required"),
});

type FormData = z.infer<typeof schema>;

export function LoginForm() {
  const { login } = useAuth();
  const {
    register,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const onSubmit = async (data: FormData) => {
    try {
      await login(data.email, data.password);
    } catch (err) {
      const msg = err instanceof ApiError ? err.message : "Login failed";
      setError("root", { message: msg });
    }
  };

  return (
    <form onSubmit={(e) => void handleSubmit(onSubmit)(e)} className="space-y-4" noValidate>
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email
        </label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          {...register("email")}
          className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          aria-invalid={errors.email ? "true" : "false"}
        />
        {errors.email && <p role="alert" className="text-xs text-red-600 mt-1">{errors.email.message}</p>}
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
          Password
        </label>
        <input
          id="password"
          type="password"
          autoComplete="current-password"
          {...register("password")}
          className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          aria-invalid={errors.password ? "true" : "false"}
        />
        {errors.password && <p role="alert" className="text-xs text-red-600 mt-1">{errors.password.message}</p>}
      </div>

      {errors.root && (
        <p role="alert" className="text-sm text-red-600 bg-red-50 rounded p-2">{errors.root.message}</p>
      )}

      <Button type="submit" isLoading={isSubmitting} className="w-full">
        Sign in
      </Button>
    </form>
  );
}
