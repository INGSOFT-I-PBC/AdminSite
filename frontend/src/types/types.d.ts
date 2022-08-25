declare global {
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
        readonly attribute: Optional<string>
        /**
         * An utility function
         */
        readonly morphFunc?: <I, O>(I) => O
        /**
         * The style class applied to the header
         */
        readonly style?: string
    }
    /**
     * This class represents the configuration of a table
     * would help to develop settings for custom tables
     */
    export class TableHeaderSettings {
        readonly headers: Array<HeaderSetup>
        readonly rows?: Array<T>
    }

    // export class Row<T> ()

    export type RowClickHandler = <T>(
        header: HeaderSetup,
        row: T?,
        index: number
    ) => void
}

export {}
