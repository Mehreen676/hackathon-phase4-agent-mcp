# REST API Spec (Phase II)

## Base
- Backend base URL (dev): http://localhost:8000
- All routes are under `/api`

## Authentication (JWT)
- Every request MUST include:
  - `Authorization: Bearer <jwt>`
- Backend verifies JWT using shared secret `BETTER_AUTH_SECRET`
- Backend must enforce user isolation:
  - Authenticated user id must match `{user_id}` in path
  - Data is filtered by authenticated user only

## Endpoints

### List tasks
GET `/api/{user_id}/tasks`

Response 200:
- array of tasks

### Create task
POST `/api/{user_id}/tasks`

Body:
- title (string, required, 1–200)
- description (string, optional, max 1000)

Response 201:
- created task

### Get task by id
GET `/api/{user_id}/tasks/{id}`

Response 200:
- task object

### Update task
PUT `/api/{user_id}/tasks/{id}`

Body:
- title (string, required)
- description (string, optional)

Response 200:
- updated task

### Delete task
DELETE `/api/{user_id}/tasks/{id}`

Response 200:
- { status: "deleted", id }

### Toggle completion
PATCH `/api/{user_id}/tasks/{id}/complete`

Response 200:
- task object with updated completed status

## Error Handling
- 401: missing/invalid JWT
- 403: user_id in URL does not match token user
- 404: task not found for that user
- 422: validation errors
