<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Todo } from './api/todos'
import { getTodos, createTodo, updateTodo, deleteTodo } from './api/todos'

const todos = ref<Todo[]>([])
const newTitle = ref('')
const loading = ref(true)
const error = ref<string | null>(null)

async function loadTodos() {
  loading.value = true
  error.value = null
  try {
    todos.value = await getTodos()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load todos'
  } finally {
    loading.value = false
  }
}

onMounted(loadTodos)

async function handleSubmit(e: Event) {
  e.preventDefault()
  const title = newTitle.value.trim()
  if (!title) return
  error.value = null
  try {
    await createTodo(title)
    newTitle.value = ''
    await loadTodos()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to add todo'
  }
}

async function toggleCompleted(todo: Todo) {
  error.value = null
  try {
    await updateTodo(todo.id, { completed: !todo.completed })
    await loadTodos()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to update todo'
  }
}

async function removeTodo(id: number) {
  error.value = null
  try {
    await deleteTodo(id)
    await loadTodos()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to delete todo'
  }
}
</script>

<template>
  <div class="todo-app">
    <h1>Todos</h1>

    <form @submit="handleSubmit" class="add-form">
      <input
        v-model="newTitle"
        type="text"
        placeholder="Add a todo..."
        aria-label="New todo title"
      />
      <button type="submit">Add</button>
    </form>

    <div v-if="error" class="error" role="alert">{{ error }}</div>
    <div v-if="loading" class="loading">Loading...</div>
    <ul v-else class="todo-list">
      <li
        v-for="todo in todos"
        :key="todo.id"
        class="todo-item"
        :class="{ completed: todo.completed }"
      >
        <input
          type="checkbox"
          :checked="todo.completed"
          @change="toggleCompleted(todo)"
          :aria-label="`Toggle ${todo.title}`"
        />
        <span class="todo-title">{{ todo.title }}</span>
        <button
          type="button"
          aria-label="Delete"
          @click="removeTodo(todo.id)"
        >
          Delete
        </button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.todo-app {
  background: var(--color-surface-elevated);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
  box-shadow: var(--shadow-lg);
}

h1 {
  font-family: var(--font-heading);
  font-size: 1.75rem;
  font-weight: 600;
  margin: 0 0 var(--space-lg);
  color: var(--color-text);
  letter-spacing: -0.02em;
}

.add-form {
  display: flex;
  gap: var(--space-sm);
  margin-bottom: var(--space-lg);
}

.add-form input {
  flex: 1;
  padding: var(--space-sm) var(--space-md);
  font-family: var(--font-body);
  font-size: 1rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-bg);
  color: var(--color-text);
  transition: border-color 0.2s, box-shadow 0.2s;
}
.add-form input::placeholder {
  color: var(--color-text-muted);
}
.add-form input:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
  border-color: var(--color-accent);
}

.add-form button {
  background: var(--color-accent);
  color: var(--color-surface-elevated);
  border-color: var(--color-accent);
}
.add-form button:hover {
  background: var(--color-accent-hover);
  border-color: var(--color-accent-hover);
}

.todo-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.todo-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md);
  margin-bottom: var(--space-xs);
  background: var(--color-bg);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s;
}
.todo-item:hover {
  box-shadow: var(--shadow-md);
}

.todo-item.completed .todo-title {
  text-decoration: line-through;
  color: var(--color-text-completed);
  opacity: 0.85;
}

.todo-title {
  flex: 1;
  font-size: 1rem;
  line-height: 1.5;
}

.todo-item input[type="checkbox"] {
  width: 1.125rem;
  height: 1.125rem;
  accent-color: var(--color-accent);
  cursor: pointer;
}
.todo-item input[type="checkbox"]:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.todo-item button {
  padding: var(--space-xs) var(--space-sm);
  font-size: 0.8125rem;
  background: transparent;
  color: var(--color-text-muted);
}
.todo-item button:hover {
  color: var(--color-error-text);
  background: var(--color-error-bg);
  border-color: var(--color-error-border);
}

.loading {
  color: var(--color-text-muted);
  padding: var(--space-md);
  text-align: center;
}

.error {
  color: var(--color-error-text);
  padding: var(--space-md);
  margin-bottom: var(--space-lg);
  background: var(--color-error-bg);
  border: 1px solid var(--color-error-border);
  border-radius: var(--radius-md);
  font-size: 0.9375rem;
}
</style>
