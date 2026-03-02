import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'
import { getTodos, createTodo, updateTodo, deleteTodo } from './todos'

vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}))

const mockedAxios = axios as unknown as {
  get: ReturnType<typeof vi.fn>
  post: ReturnType<typeof vi.fn>
  patch: ReturnType<typeof vi.fn>
  delete: ReturnType<typeof vi.fn>
}

describe('todos API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('getTodos fetches from /todos', async () => {
    const todos = [{ id: 1, title: 'Test', completed: false, created_at: '2025-01-01T00:00:00Z' }]
    mockedAxios.get.mockResolvedValue({ data: todos })

    const result = await getTodos()

    expect(mockedAxios.get).toHaveBeenCalledWith('/todos')
    expect(result).toEqual(todos)
  })

  it('createTodo POSTs title to /todos', async () => {
    const created = { id: 1, title: 'New todo', completed: false, created_at: '2025-01-01T00:00:00Z' }
    mockedAxios.post.mockResolvedValue({ data: created })

    const result = await createTodo('New todo')

    expect(mockedAxios.post).toHaveBeenCalledWith('/todos', { title: 'New todo' })
    expect(result).toEqual(created)
  })

  it('updateTodo PATCHes to /todos/:id with partial body', async () => {
    const updated = { id: 1, title: 'Updated', completed: true, created_at: '2025-01-01T00:00:00Z' }
    mockedAxios.patch.mockResolvedValue({ data: updated })

    const result = await updateTodo(1, { completed: true })

    expect(mockedAxios.patch).toHaveBeenCalledWith('/todos/1', { completed: true })
    expect(result).toEqual(updated)
  })

  it('updateTodo sends title when provided', async () => {
    mockedAxios.patch.mockResolvedValue({ data: {} })

    await updateTodo(1, { title: 'New title' })

    expect(mockedAxios.patch).toHaveBeenCalledWith('/todos/1', { title: 'New title' })
  })

  it('deleteTodo DELETEs /todos/:id', async () => {
    mockedAxios.delete.mockResolvedValue({ status: 204 })

    await deleteTodo(1)

    expect(mockedAxios.delete).toHaveBeenCalledWith('/todos/1')
  })
})
