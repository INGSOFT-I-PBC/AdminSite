import type { Sequence } from '@store-types'
import axios from 'axios'

class SequenceDataService {
    async fetchSequence(name: string) {
        return (await axios.get<Sequence>(`/api/v1/sequence?name=${name}`)).data
    }

    /**
     * Edit the data of an specific Sequence into the backend.
     *
     * @param name the Id of the sequence to edit
     * @param data the data to overwrite
     * @returns the response of the backend
     */
    async editSequence(name: string, data: Sequence) {
        return (
            await axios.put<Sequence>(`/api/v1/sequence?name=${name}`, data)
        ).data
    }
}
export default new SequenceDataService()
