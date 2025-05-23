import '@testing-library/jest-dom'
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import * as matchers from '@testing-library/jest-dom/matchers'

declare global {
  namespace Vi {
    interface JestAssertion extends matchers.TestingLibraryMatchers<any, void> {}
  }
}

expect.extend(matchers)

afterEach(() => {
  cleanup()
})