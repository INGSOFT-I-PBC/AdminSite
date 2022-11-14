import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import ECard from '../custom/ECard.vue'

// Dummy test to test a Card Element
describe('ECard', () => {
    it('renders properly', () => {
        const wrapper = mount(ECard)
        // Check if its a div container
        expect(wrapper.element).toContain(HTMLDivElement)
        expect(wrapper.props).toContain([])
    })
})
