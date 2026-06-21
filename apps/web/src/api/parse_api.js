
import request from '../util/request'
import axios from 'axios'

const url='/parse_json_file'
export function getJson(filePath) {
    return request.post(
        url,
        filePath
    )    
}