import axios, { Axios, type AxiosResponse } from 'axios'
import type Item from '@/interfaz/items'

/* eslint-disable */
class ItemDataService {
    var: string =
        'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY0NDk1MTk0LCJpYXQiOjE2NjQ0NjYzOTQsImp0aSI6IjdhYjRmMWM2MDAxODQyZjNhNGY5NGRlZjY4Yjg5OGFmIiwidXNlcl9pZCI6M30.USRfAbA-cAmUPO5UVOBlZ_BP7so3SGwZqf1MqTqBDD11tNa6L9rcam7k-2rzFy7aa5HemxhxA0SaVFSqNyEloa6J5tAXN6Zh-UneKQMQiU-fSAJk8upjWfvRSUbO3TbbuVPlZuAKTl1-o-WCvR-sxXzCf6ip7MwcBBR_6n-2NabhpG-KIkd1Mi4KcRi8X3dpJSPfT_5HoLyNceJa5L2aoq6Mm6KJJ7b4Sz7O_2Pz9uKzDtAOU5BwKXZtKJ2K6EpDLs8gTzLDpfza3rcP1MCYV_0BnkB6_APlbOXZ-PQ6IIae0gCw4__uDcnQQB3qx1NusWm6Uf6d169Ghqqr_F7YLMU3hKL0EU4iBjhvDJ7ucux7PY68zMwxPNm8KrnD5WCF13p5PLZQqe3Xu_p1DH0MsI1c3xA4Teif1C0j4Ml-eCNMPI_NG90mT66WdpIe9j5uOk-3gyMIi6XYuupWl1lJxXlGR48XLexYjSt28id4Nq8dMXGgY_Jvn1q5kaIRCHFfmUgm74umuonTu0HmRTB1dL8mIswUKoBQyJX6v9KtZpIIryUGu0Wf394ONIbNFRCy5qh8C106mlRCm8snCREEq7PQ-2YOXSyMcq_fQnN2hnFaXiTJJUrK7_KBmKVd3lsZ4UABb9g09Ae17xiPHmXrKnJHcmY43h_NLntSFL0YJaM'
    async getAll(): Promise<any> {
        return await axios.get('/api/v1/inventory', {
            headers: {
                'Content-Type': 'application/json',
               // Authorization: this.var,
            },
        })
    }

    async get(id: string): Promise<AxiosResponse<Item>> {
        return await axios.get(`/api/v1/items/${id}`, {
            headers: {
                'Content-Type': 'application/json',
                //Authorization: this.var,
            },
        })
    }

    createItem(data: any): Promise<any> {
        return axios
            .post('/api/v1/items', data, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    //Authorization: this.var,
                    //'cache-control': 'no-cache',
                    //'content-type': 'application/x-www-form-urlencoded',
                },
            })
            .then(response => {
                console.log('Successfully uploaded: ', response.data)
            })
            .catch(err => {
                console.log('error occured: ', err)
            })
    }
    createInventory(data: any): Promise<any> {
        return axios.post(
            '/api/v1/inventory',
            {
                headers: {
                    //Authorization: this.var,
                    'Content-Type': 'multipart/form-data',
                },
            },
            data
        )
    }

    update(id: any, data: any): Promise<any> {
        return axios.put(
            `/api/v1/items/${id}`,
            {
                headers: {
                    //Authorization: this.var,
                },
            },
            data
        )
    }

    delete(id: any): Promise<any> {
        return axios.delete(`/api/v1/items/${id}`, {
            headers: {
                Authorization: this.var,
            },
        })
    }
}

export default new ItemDataService()
