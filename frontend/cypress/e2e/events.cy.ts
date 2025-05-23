describe('Events', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  it('displays event list', () => {
    cy.contains('Upcoming Events').should('be.visible')
    cy.get('[data-testid="event-card"]').should('have.length.greaterThan', 0)
  })

  it('filters events by category', () => {
    cy.get('[data-testid="category-filter"]').click()
    cy.get('[data-value="conference"]').click()
    cy.get('[data-testid="event-card"]').each(($el) => {
      cy.wrap($el).contains('conference')
    })
  })

  it('searches events', () => {
    cy.get('[data-testid="search-input"]').type('Tech')
    cy.get('[data-testid="event-card"]').should('contain', 'Tech')
  })

  it('navigates to event details', () => {
    cy.get('[data-testid="event-card"]').first().click()
    cy.url().should('include', '/events/')
    cy.contains('Register').should('be.visible')
  })
})

describe('Event Registration', () => {
  beforeEach(() => {
    cy.login('testuser', 'testpassword')
    cy.visit('/events/1')
  })

  it('registers for an event', () => {
    cy.contains('Register').click()
    cy.contains('Registered for event successfully').should('be.visible')
  })

  it('cancels registration', () => {
    cy.contains('Cancel Registration').click()
    cy.contains('Yes, Cancel').click()
    cy.contains('Registration cancelled').should('be.visible')
  })
})