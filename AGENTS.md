# AGENTS.md

## Purpose
This project uses Spec-Driven Development (SDD). No code is written until the spec is complete and approved.

## Workflow (Source of Truth)
1) Constitution/Rules (this file)
2) Specify (WHAT): specs/...
3) Plan (HOW): specs/architecture.md
4) Tasks (BREAKDOWN): specs/history/... (versions of specs as they evolve)
5) Implement (CODE): only after tasks/spec are clear

## Non-Negotiables
- Use the required Phase II stack:
  - Frontend: Next.js (App Router) + TypeScript + Tailwind
  - Backend: FastAPI + SQLModel
  - DB: Neon Serverless Postgres
  - Auth: Better Auth (JWT)
- All REST endpoints must be protected by JWT and must only access the authenticated user’s tasks.
- Any change in behavior requires updating specs first.

## Quality Bar (UI)
- UI must look professional: modern layout, clear typography, consistent spacing, responsive, polished components.
- No “default/basic” looking pages. Use a clean dashboard layout and good component styling.

## How to Work With the Agent
- Always reference a spec file when asking for implementation.
- If something is unclear, update specs instead of guessing.
