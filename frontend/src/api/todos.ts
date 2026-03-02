import axios from 'axios'

const base = (import.meta.env.VITE_API_BASE as string) || ''
const url = (path: string) => `${base}${path}`

export interface Todo {
  id: number
  title: string
  completed: boolean
  created_at: string
}

export interface TodoUpdate {
  title?: string
  completed?: boolean
}

export async function getTodos(): Promise<Todo[]> {
  const { data } = await axios.get<Todo[]>(url('/todos'))
  return data
}

export async function createTodo(title: string): Promise<Todo> {
  const { data } = await axios.post<Todo>(url('/todos'), { title })
  return data
}

export async function updateTodo(id: number, body: TodoUpdate): Promise<Todo> {
  const { data } = await axios.patch<Todo>(url(`/todos/${id}`), body)
  return data
}

export async function deleteTodo(id: number): Promise<void> {
  await axios.delete(url(`/todos/${id}`))
}
