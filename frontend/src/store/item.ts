import axios,{Axios, type AxiosResponse } from 'axios'
import type Item from '@/interfaz/items'

/* eslint-disable */
class ItemDataService {
    var: string =
        'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYzOTc5OTA5LCJpYXQiOjE2NjM5NTExMDksImp0aSI6IjU1MTM4NGUyODdhMjQzZGJiMjk5Zjk1MWEwN2I2YWU5IiwidXNlcl9pZCI6M30.fUfkHzP3Y5FrwGqMtdjQBcc1ZlaVDKQVCydACuV9bPfbO8JBa1iF8SzzaOl_-1MLrt_cvRf6JM_R9AvcoupbYdTZbRf8xUJdawPi2M8OqttMiQEqQ49sqxdhk7jgXaHe6RWP1vU3a74Wwrza-CFWOdE8_EmKD7_17fgjN6WfbMBgNqH3fotfdmEMhI-HACh2c86LFbzljxcAIxpZBEPRZ-b07Pm3hYeaeX7lEeuj5JU4rsgGMltujv1c9oEtsUJFvf1YiRRgpheEoYpIlrtKQxa6_mUW84lWJLz3NVqW_-6rwLXsxkP2sm1A-cj3W1pcJt2ImgT4J_6hxZ0_oaLlmjiRgl7fcoypgrqFueQKB01I5flDbHTJzK5EtbNUUVUVqUnsXl1edVgoJ3qEtmhw-f76yTj89yKVryX4ZQ_FTaiKOHl4YjuQpzTX7nOFDL5OtI9kiYsWzzfbnXNICg3U8tRHDKQB9hJR28n7QIPfH7beG9EseC1tnB_1OlwZ9CL9QtOJ8X_Nbm_BPKLI8tV3oqLaQSF29Nfr_E5E9eNGqA47XLDxMwh9MJnPCev6x68oWMaktEaxiiulSDTPxl78A4XBH0klxqZVLIvHMBl8IXHiLdNi6YgEv6hV_YjE42kfhbMz-BQ0XJVaQXFdYY2b9-LZ19CfEutpOP12S1u5eWA'
    async getAll(): Promise<any> {
        return await axios.get('/api/v1/inventory', {
            headers: {
                "Content-Type":"application/json",
                Authorization: this.var,
            },
        })
    }

    async get(id: string): Promise<AxiosResponse<Item>> {
        return await axios.get(`/api/v1/items/${id}`, {
            headers: {
                "Content-Type":"application/json",
                Authorization: this.var,
            },
        })
    }

    create(data: any): Promise<any> {
        return axios.post(
            '/api/v1/items',
            {
                headers: {
                    Authorization: this.var,
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
                    Authorization: this.var,
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
