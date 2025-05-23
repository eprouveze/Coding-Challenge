/// <reference types="cypress" />

declare global {
  namespace Cypress {
    interface Chainable {
      login(username: string, password: string): Chainable<void>
    }
  }
}

Cypress.Commands.add('login', (username: string, password: string) => {
  cy.request('POST', 'http://localhost:8000/users/token', {
    username,
    password,
  }).then((response) => {
    window.localStorage.setItem('auth-storage', JSON.stringify({
      state: {
        token: response.body.access_token,
        isAuthenticated: true,
      },
    }))
  })
})

export {}