export type ComponentSize = 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | 'full'
type Elevation = 'sm' | 'md' | 'lg' | 'xl' | 'xxl' | 'none' | ''
export type BorderRadius =
    | 'sm'
    | 'md'
    | 'lg'
    | 'xl'
    | 'xxl'
    | 'none'
    | ''
    | 'xxxl'
    | 'full'

export type TextColorMode =
    | 'auto'
    | 'dark'
    | 'night'
    | 'light'
    | 'danger'
    | 'success'
    | 'none'
    | ''

export type ColorTheme =
    | 'auto'
    | 'none'
    | 'outline'
    | 'daynight'
    | 'light'
    | 'light-auto'
    | 'dark'
    | 'dark-auto'

export type Orientation = 'horizontal' | 'vertical'

export type VerticalAlignment =
    | 'start'
    | 'end'
    | 'baseline'
    | 'stretch'
    | 'middle'
export type HorizontalAlignment =
    | 'start'
    | 'center'
    | 'end'
    | 'around'
    | 'between'
    | 'none'
export type Alignment = VerticalAlignment | HorizontalAlignment
export type Booleanish = 'true' | 'false' | '' | boolean

export type InputType =
    | 'text'
    | 'checkbox'
    | 'button'
    | 'color'
    | 'date'
    | 'datetime'
    | 'datetime-local'
    | 'email'
    | 'file'
    | 'hidden'
    | 'image'
    | 'month'
    | 'number'
    | 'password'
    | 'radio'
    | 'range'
    | 'reset'
    | 'search'
    | 'submit'
    | 'tel'
    | 'time'
    | 'url'
    | 'week'

export default Elevation
