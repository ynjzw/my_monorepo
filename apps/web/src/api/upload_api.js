
import request from '../util/request'
import axios from 'axios'

const upload_url='/routes/upload_api/upload'
export function uploadFile(data){
    return request.post(
        upload_url,
        data
    )    
}
