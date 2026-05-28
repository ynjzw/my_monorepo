
import request from '../util/request'
import axios from 'axios'

const chat_url='/chat'
export function chat(data){
    return request.post(
        chat_url,
        data
    )    
}

const speechtotext_url='/speechtotext'
export function speechtotext(){
    return request({
        url:speechtotext_url,
        method:'get'
    })    
}

const extract_triples_url='/extract_triples'
export function extract_triples(text){
    return request.post(
        extract_triples_url,
        text
    )    
}