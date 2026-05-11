// FRONTEND_AGENT | 2026-05-10 | Registration form with validation
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useAuth } from "@/hooks/useAuth";
import { Button } from "@/components/common/Button";
import { ApiError } from "@/api/client";

const schema = z
  .object({
    email: z.string().email("Invalid email"),
    password: z.string().min(8, "Password must be at least 8 characters"),
    confirm: z.string(),
  })
  .refine((d) => d.password === d.confirm, {
    message: "Passwords do not match",
    path: ["confirm"],
  });

type FormData = z.infer<typeof schema>;

export function RegisterForm() {
  const { register: registerUser } = useAuth();
  const {
    register,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const onSubmit = async (data: FormData) => {
    try {
      await registerUser(data.email, data.password);
    } catch (err) {
      const msg = err instanceof ApiError ? err.message : "Registration failed";
      setError("root", { message: msg });
    }
  };

  return (
    <form onSubmit={(e) => void handleSubmit(onSubmit)(e)} className="space-y-4" noValidate>
      {(["email", "password", "confirm"] as const).map((field) => (
        <div key={field}>
          <label htmlFor={field} className="block text-sm font-medium text-gray-700 mb-1">
            {field === "confirm" ? "Confirm password" : field.charAt(0).toUpperCase() + field.slice(1)}
          </label>
          <input
            id={field}
            type={field === "email" ? "email" : "password"}
            {...register(field)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            aria-invalid={errors[field] ? "true" : "false"}
          />
          {errors[field] && <p role="alert" className="text-xs text-red-600 mt-1">{errors[field]?.message}</p>}
        </div>
      ))}

      {errors.root && (
        <p role="alert" className="text-sm text-red-600 bg-red-50 rounded p-2">{errors.root.message}</p>
      )}

      <Button type="submit" isLoading={isSubmitting} className="w-full">
        Create account
      </Button>
    </form>
  );
}
