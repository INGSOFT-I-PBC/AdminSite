export interface HeaderSetup {
    /**
     * The label that is show on the header of the
     * table
     */
    readonly label: string
    /**
     * The attribute that will be show on the table.
     * If `morphFunc` is provided the attribute must be
     * the attribute of the result object.
     */
    attribute: Optional<string>
    /**
     * An utility function
     */
    morphFunc?: <I, O>(input: I) => O
    /**
     * The style class applied to the header
     */
    style?: string
}
/**
 * This class represents the configuration of a table
 * would help to develop settings for custom tables
 */
export class TableHeaderSettings {
    headers: Array<HeaderSetup>
    rows?: Array<unknown>

    constructor() {
        this.headers = []
    }
}

// export class Row<T> ()

export type RowClickHandler = <T>(
    header: HeaderSetup,
    row: T | null,
    index: number
) => void

export default {}
