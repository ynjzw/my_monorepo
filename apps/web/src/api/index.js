
import request from '../util/request'
import axios from 'axios'

const url = '/books'
export function getBooks(){
    // return request.get('http://localhost:8000/books')
    return request({
        url:url,
        method:'get'
    })    
}
// export const getBooks=()=>ge('/books')

export function postBook(bookName,bookAuthor){
    return request.post(url,{'name':bookName,'author':bookAuthor})
}

const url1='/nodes'
export function getNodes(){
    // return request.get('http://localhost:8000/books')
    return request({
        url:url1,
        method:'get'
    })    
}

const url2='/link'
export function getLink(){
    // return request.get('http://localhost:8000/books')
    return request({
        url:url2,
        method:'get'
    })    
}

const url3='/world'
export function getWorld(){
    // return request.get('http://localhost:8000/books')
    return request({
        url:url3,
        method:'get'
    })    
}


const url6='/family'
export function getFamily(){
    return request({
        url:url6,
        method:'get'
    })    
}

const url4='/upload'
export function uploadFile(data){
    return request.post(
        url4,
        data
    )    
}

const url5='/chat'
export function chat(data){
    return request.post(
        url5,
        data
    )    
}

const url7='/speechtotext'
export function speechtotext(){
    return request({
        url:url7,
        method:'get'
    })    
}

const url8='/base_nodes'
export function get_base_nodes(){
    return request({
        url:url8,
        method:'get'
    })    
}

const url9='/maslow_needs'
export function get_maslow_needs(){
    return request({
        url:url9,
        method:'get'
    })    
}

const old_structure_url='/old_structure'
export function get_old_structure(){
    return request({
        url:old_structure_url,
        method:'get'
    })    
}

const new_structure_url='/new_structure'
export function get_new_structure(){
    return request({
        url:new_structure_url,
        method:'get'
    })    
}


const solar='/solar'
export function get_solar(){
    return request({
        url:solar,
        method:'get'
    })    
}