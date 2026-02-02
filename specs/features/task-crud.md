# Feature: Task CRUD (Phase II)

## User Stories
- As a user, I can add a new task with title and optional description
- As a user, I can view my tasks list
- As a user, I can update a task
- As a user, I can delete a task
- As a user, I can mark a task as complete/incomplete
- As a user, I can only see and manage my own tasks (multi-user isolation)

## Acceptance Criteria

### Create Task
- Title required (1–200 chars)
- Description optional (0–1000 chars)
- Task saved to database with user_id from JWT
- Returns created task

### View Tasks
- Returns tasks only for authenticated user
- Each task shows:
  - title
  - description (if present)
  - completed status
  - created_at

### Update Task
- Only owner can update
- Title + description update
- updated_at changes

### Delete Task
- Only owner can delete
- Returns confirmation response

### Toggle Complete
- Only owner can toggle
- Completed flips true/false
- Returns updated task

## UI Requirements (for this feature)
- Dashboard lists tasks in a clean card layout
- Add/Edit uses modal form with validation
- Immediate UI feedback: loaders + toast messages
- Empty state when no tasks
