// FRONTEND_AGENT | 2026-05-10 | Reusable Button component
import { type ButtonHTMLAttributes, forwardRef } from "react";
import { Spinner } from "./Spinner";

type Variant = "primary" | "secondary" | "danger" | "ghost";
type Size = "sm" | "md" | "lg";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  isLoading?: boolean;
}

const variantClasses: Record<Variant, string> = {
  primary: "bg-blue-600 hover:bg-blue-700 text-white border-transparent",
  secondary: "bg-white hover:bg-gray-50 text-gray-700 border-gray-300",
  danger: "bg-red-600 hover:bg-red-700 text-white border-transparent",
  ghost: "bg-transparent hover:bg-gray-100 text-gray-600 border-transparent",
};

const sizeClasses: Record<Size, string> = {
  sm: "px-3 py-1.5 text-sm",
  md: "px-4 py-2 text-sm",
  lg: "px-6 py-3 text-base",
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = "primary", size = "md", isLoading, children, disabled, className = "", ...props }, ref) => (
    <button
      ref={ref}
      disabled={disabled ?? isLoading}
      className={`inline-flex items-center justify-center gap-2 rounded-md border font-medium
        transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
        disabled:opacity-50 disabled:cursor-not-allowed
        ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      {...props}
    >
      {isLoading && <Spinner size="sm" />}
      {children}
    </button>
  )
);
Button.displayName = "Button";
