import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import App from './App.vue'
import * as todosApi from './api/todos'

vi.mock('./api/todos', () => ({
  getTodos: vi.fn(),
  createTodo: vi.fn(),
  updateTodo: vi.fn(),
  deleteTodo: vi.fn(),
}))

const mockGetTodos = vi.mocked(todosApi.getTodos)
const mockCreateTodo = vi.mocked(todosApi.createTodo)
const mockUpdateTodo = vi.mocked(todosApi.updateTodo)
const mockDeleteTodo = vi.mocked(todosApi.deleteTodo)

const mockTodos = [
  { id: 1, title: 'Todo 1', completed: false, created_at: '2025-01-01T00:00:00Z' },
  { id: 2, title: 'Todo 2', completed: true, created_at: '2025-01-01T00:00:00Z' },
]

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetTodos.mockResolvedValue(mockTodos)
  })

  it('renders add form with input and button', async () => {
    const wrapper = mount(App)
    await wrapper.vm.$nextTick()

    expect(wrapper.find('input[type="text"]').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('loads todos on mount', async () => {
    mount(App)
    await vi.waitFor(() => expect(mockGetTodos).toHaveBeenCalledTimes(1))
  })

  it('displays list of todos with title and completed state', async () => {
    const wrapper = mount(App)
    await vi.waitFor(() => expect(wrapper.text()).toContain('Todo 1'))

    expect(wrapper.text()).toContain('Todo 2')
    const checkboxes = wrapper.findAll('input[type="checkbox"]')
    expect(checkboxes.length).toBeGreaterThanOrEqual(2)
    expect((checkboxes[1]!.element as HTMLInputElement).checked).toBe(true) // Todo 2 is completed
  })

  it('shows strikethrough for completed todos', async () => {
    const wrapper = mount(App)
    await vi.waitFor(() => expect(wrapper.find('.completed').exists()).toBe(true))

    const completedLabel = wrapper.find('.completed')
    expect(completedLabel.exists()).toBe(true)
    expect(completedLabel.text()).toContain('Todo 2')
  })

  it('does not call createTodo when form is submitted with empty title', async () => {
    const wrapper = mount(App)
    await vi.waitFor(() => expect(wrapper.text()).toContain('Todo 1'))

    await wrapper.find('form').trigger('submit')

    expect(mockCreateTodo).not.toHaveBeenCalled()
  })

  it('creates todo when form is submitted', async () => {
    mockCreateTodo.mockResolvedValue({
      id: 3,
      title: 'New todo',
      completed: false,
      created_at: '2025-01-01T00:00:00Z',
    })
    mockGetTodos.mockResolvedValue([...mockTodos, { id: 3, title: 'New todo', completed: false, created_at: '2025-01-01T00:00:00Z' }])

    const wrapper = mount(App)
    await vi.waitFor(() => expect(wrapper.text()).toContain('Todo 1'))

    const input = wrapper.find('input[type="text"]')
    await input.setValue('New todo')
    await wrapper.find('form').trigger('submit')

    expect(mockCreateTodo).toHaveBeenCalledWith('New todo')
    await vi.waitFor(() => expect(wrapper.text()).toContain('New todo'))
    expect(wrapper.findAll('.todo-item').length).toBe(3)
  })

  it('toggles completed when checkbox is clicked', async () => {
    mockUpdateTodo.mockResolvedValue({
      id: 1,
      title: 'Todo 1',
      completed: true,
      created_at: '2025-01-01T00:00:00Z',
    })
    const updatedTodos = [
      { id: 1, title: 'Todo 1', completed: true, created_at: '2025-01-01T00:00:00Z' },
      mockTodos[1]!,
    ]
    mockGetTodos.mockResolvedValueOnce(mockTodos).mockResolvedValueOnce(updatedTodos)

    const wrapper = mount(App)
    await vi.waitFor(() => expect(wrapper.text()).toContain('Todo 1'))

    const checkboxes = wrapper.findAll('input[type="checkbox"]')
    await checkboxes[0]!.trigger('change')

    expect(mockUpdateTodo).toHaveBeenCalledWith(1, { completed: true })
    await vi.waitFor(() => expect(wrapper.find('.todo-item.completed').text()).toContain('Todo 1'))
  })

  it('deletes todo when delete button is clicked', async () => {
    mockDeleteTodo.mockResolvedValue(undefined)
    mockGetTodos
      .mockResolvedValueOnce(mockTodos)
      .mockResolvedValueOnce([mockTodos[1]!])

    const wrapper = mount(App)
    await vi.waitFor(() => expect(wrapper.find('button[aria-label="Delete"]').exists()).toBe(true))

    const deleteBtn = wrapper.find('button[aria-label="Delete"]')
    await deleteBtn.trigger('click')

    expect(mockDeleteTodo).toHaveBeenCalledWith(1)
    await vi.waitFor(() => expect(wrapper.text()).not.toContain('Todo 1'))
    expect(wrapper.findAll('.todo-item').length).toBe(1)
  })

  it('displays empty list when no todos', async () => {
    mockGetTodos.mockResolvedValue([])

    const wrapper = mount(App)
    await vi.waitFor(() => expect(wrapper.find('.loading').exists()).toBe(false))

    expect(wrapper.findAll('.todo-item').length).toBe(0)
  })

  it('displays error when load fails', async () => {
    mockGetTodos.mockRejectedValue(new Error('Network error'))

    const wrapper = mount(App)
    await vi.waitFor(() => expect(wrapper.find('[role="alert"]').exists()).toBe(true))

    expect(wrapper.find('[role="alert"]').text()).toBe('Network error')
  })

  it('displays error when add fails', async () => {
    mockCreateTodo.mockRejectedValue(new Error('Add failed'))

    const wrapper = mount(App)
    await vi.waitFor(() => expect(wrapper.text()).toContain('Todo 1'))

    const input = wrapper.find('input[type="text"]')
    await input.setValue('New todo')
    await wrapper.find('form').trigger('submit')

    await vi.waitFor(() => expect(wrapper.find('[role="alert"]').exists()).toBe(true))
    expect(wrapper.find('[role="alert"]').text()).toBe('Add failed')
  })

  it('displays error when toggle fails', async () => {
    mockUpdateTodo.mockRejectedValue(new Error('Update failed'))

    const wrapper = mount(App)
    await vi.waitFor(() => expect(wrapper.text()).toContain('Todo 1'))

    const checkboxes = wrapper.findAll('input[type="checkbox"]')
    await checkboxes[0]!.setValue(true)

    await vi.waitFor(() => expect(wrapper.find('[role="alert"]').exists()).toBe(true))
    expect(wrapper.find('[role="alert"]').text()).toBe('Update failed')
  })

  it('displays error when delete fails', async () => {
    mockDeleteTodo.mockRejectedValue(new Error('Delete failed'))

    const wrapper = mount(App)
    await vi.waitFor(() => expect(wrapper.find('button[aria-label="Delete"]').exists()).toBe(true))

    const deleteBtn = wrapper.find('button[aria-label="Delete"]')
    await deleteBtn.trigger('click')

    await vi.waitFor(() => expect(wrapper.find('[role="alert"]').exists()).toBe(true))
    expect(wrapper.find('[role="alert"]').text()).toBe('Delete failed')
  })
})
