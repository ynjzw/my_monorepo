
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

const url2='/links'
export function getLinks(){
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

const url4='/uploadFile'
export function uploadFile(data){
    return request.post(
        url4,
        {'data':data}
    )    
}


const url6='/family'
export function getFamily(){
    return request({
        url:url6,
        method:'get'
    })    
}
