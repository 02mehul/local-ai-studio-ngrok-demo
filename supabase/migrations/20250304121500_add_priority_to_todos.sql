-- Add priority column to todos table
-- This allows tasks to be ranked by importance.
-- Default is 0, which represents 'normal' priority.

ALTER TABLE IF EXISTS public.todos 
ADD COLUMN IF NOT EXISTS priority integer DEFAULT 0;

-- Add an index to optimize sorting by priority
CREATE INDEX IF NOT EXISTS idx_todos_priority ON public.todos (priority DESC, id DESC);