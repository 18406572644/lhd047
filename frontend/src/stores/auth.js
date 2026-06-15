import { writable } from 'svelte/store'

function createAuthStore() {
  const storedToken = localStorage.getItem('token')
  const storedUser = localStorage.getItem('user')

  const { subscribe, set, update } = writable({
    token: storedToken || '',
    user: storedUser ? JSON.parse(storedUser) : null,
    isAuthenticated: !!storedToken
  })

  return {
    subscribe,
    login(token, user) {
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify(user))
      set({ token, user, isAuthenticated: true })
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      set({ token: '', user: null, isAuthenticated: false })
    },
    updateUser(user) {
      localStorage.setItem('user', JSON.stringify(user))
      update(state => ({ ...state, user }))
    }
  }
}

export const auth = createAuthStore()
