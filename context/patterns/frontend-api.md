---
auto-captured: true
tags: [pattern, frontend, api, vue]
scope: frontend
summary: Vue 3 Composition API with axios, VITE_API_BASE for dev/prod, mocked API in tests
---

# Frontend API Pattern

## What

API layer in `src/api/todos.ts` using axios. Base URL from `import.meta.env.VITE_API_BASE || ''` so dev uses proxy (empty → `/todos`) and prod uses `/api` → `/api/todos`. Component tests mock the API module, not axios.

## Implementation

```typescript
// frontend/src/api/todos.ts
const base = (import.meta.env.VITE_API_BASE as string) || ''

export async function getTodos(): Promise<Todo[]> {
  const { data } = await axios.get<Todo[]>(`${base}/todos`)
  return data
}
```

## Key Decisions

- Mock `./api/todos` in component tests; avoids HTTP details, focuses on UI.
- `todos.spec.ts` mocks axios directly for API module tests.
- Error handling: `App.vue` catches and displays via `error` ref and `role="alert"`.
