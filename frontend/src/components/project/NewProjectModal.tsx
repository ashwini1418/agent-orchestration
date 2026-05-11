// FRONTEND_AGENT | 2026-05-10 | New project creation modal
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useNavigate } from "react-router-dom";
import { Modal } from "@/components/common/Modal";
import { Button } from "@/components/common/Button";
import { sessionsApi } from "@/api/sessions";
import { useProjects } from "@/hooks/useProjects";

const schema = z.object({
  name: z.string().min(1, "Name required").max(255),
  description: z.string().min(10, "Description must be at least 10 characters").max(10_000),
  output_dir_name: z.string().max(64).regex(/^[a-zA-Z0-9_\-]*$/, "Only letters, numbers, _ and -").optional(),
});

type FormData = z.infer<typeof schema>;

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export function NewProjectModal({ isOpen, onClose }: Props) {
  const { createProject } = useProjects();
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    setError,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const onSubmit = async (data: FormData) => {
    try {
      const project = await createProject(data);
      const session = await sessionsApi.create(project.id);
      reset();
      onClose();
      navigate(`/session/${session.id}`);
    } catch {
      setError("root", { message: "Failed to create project" });
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="New Project">
      <form onSubmit={(e) => void handleSubmit(onSubmit)(e)} className="space-y-4">
        <div>
          <label htmlFor="proj-name" className="block text-sm font-medium text-gray-700 mb-1">
            Project name
          </label>
          <input
            id="proj-name"
            {...register("name")}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="My Awesome App"
          />
          {errors.name && <p role="alert" className="text-xs text-red-600 mt-1">{errors.name.message}</p>}
        </div>

        <div>
          <label htmlFor="proj-desc" className="block text-sm font-medium text-gray-700 mb-1">
            Description <span className="text-gray-400">(be specific — agents use this)</span>
          </label>
          <textarea
            id="proj-desc"
            {...register("description")}
            rows={4}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            placeholder="A fullstack todo app with React frontend and FastAPI backend, PostgreSQL database, JWT auth..."
          />
          {errors.description && <p role="alert" className="text-xs text-red-600 mt-1">{errors.description.message}</p>}
        </div>

        {errors.root && (
          <p role="alert" className="text-sm text-red-600 bg-red-50 rounded p-2">{errors.root.message}</p>
        )}

        <div className="flex justify-end gap-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancel</Button>
          <Button type="submit" isLoading={isSubmitting}>
            Create & Launch Agents
          </Button>
        </div>
      </form>
    </Modal>
  );
}
