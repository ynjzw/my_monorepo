
import request from '../util/request'
import axios from 'axios'

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


const url_population_structure='/population_structure'
export function population_structure(year){
    return request({
        url:url_population_structure,
        method:'get'
    })    
}