ALTER TABLE public.todos
ADD COLUMN IF NOT EXISTS created_at timestamptz DEFAULT now();
