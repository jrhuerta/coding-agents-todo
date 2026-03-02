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
  max-width: 32rem;
  margin: 2rem auto;
  padding: 1rem;
}

h1 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.add-form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.add-form input {
  flex: 1;
  padding: 0.5rem;
  font-size: 1rem;
}

.add-form button {
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.todo-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.todo-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.todo-item.completed .todo-title {
  text-decoration: line-through;
  color: #888;
}

.todo-title {
  flex: 1;
}

.todo-item button {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
}

.loading {
  color: #666;
}

.error {
  color: #c00;
  padding: 0.5rem;
  margin-bottom: 1rem;
  background: #fee;
  border-radius: 0.25rem;
}
</style>
