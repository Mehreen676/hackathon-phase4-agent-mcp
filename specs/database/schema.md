# Database Schema (Phase II)

## Database
- Neon Serverless PostgreSQL
- Connection string via env: `DATABASE_URL`

## Tables

### users (managed by Better Auth)
- id: string (primary key)
- email: string (unique)
- name: string (nullable)
- created_at: timestamp

### tasks
- id: integer (primary key, auto-increment)
- user_id: string (foreign key -> users.id, required)
- title: string (not null)
- description: text (nullable)
- completed: boolean (default false)
- created_at: timestamp (default now)
- updated_at: timestamp (auto update)

## Indexes
- tasks.user_id (for user filtering)
- tasks.completed (for status filtering)
