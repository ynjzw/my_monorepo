
import request from '../util/request'
import axios from 'axios'

const url1='/routes/simple_api/nodes'
export function getNodes(){
    // return request.get('http://localhost:8000/books')
    return request({
        url:url1,
        method:'get'
    })    
}

const url_liveCycle='/routes/simple_api/liveCycle'
export function getLiveCycle(){
    // return request.get('http://localhost:8000/books')
    return request({
        url:url_liveCycle,
        method:'get'
    })    
}

const url2='/routes/simple_api/link'
export function getLink(){
    // return request.get('http://localhost:8000/books')
    return request({
        url:url2,
        method:'get'
    })    
}

const url3='/routes/simple_api/world'
export function getWorld(){
    // return request.get('http://localhost:8000/books')
    return request({
        url:url3,
        method:'get'
    })    
}


const url6='/routes/simple_api/family'
export function getFamily(){
    return request({
        url:url6,
        method:'get'
    })    
}


const url8='/routes/simple_api/base_nodes'
export function get_base_nodes(node_type){
    return request({
        url:url8,
        method:'get',
        params: {
            node_type: node_type
        }
    })    
}

const url9='/routes/simple_api/maslow_needs'
export function get_maslow_needs(){
    return request({
        url:url9,
        method:'get'
    })    
}

const url_personal_data='/routes/simple_api/personal_data'
export function get_personal_data(){
    return request({
        url:url_personal_data,
        method:'get'
    })    
}

const url_update_personal_data='/routes/simple_api/update_personal_data'
export function update_personal_data(data){
    return request({
        url:url_update_personal_data,
        method:'post',
        data:data
    })    
}

const old_structure_url='/routes/simple_api/old_structure'
export function get_old_structure(){
    return request({
        url:old_structure_url,
        method:'get'
    })    
}

const new_structure_url='/routes/simple_api/new_structure'
export function get_new_structure(){
    return request({
        url:new_structure_url,
        method:'get'
    })    
}


const solar='/routes/simple_api/solar'
export function get_solar(){
    return request({
        url:solar,
        method:'get'
    })    
}

const url_population_structure='/routes/simple_api/population_structure'
export function population_structure(year){
    return request({
        url:url_population_structure,
        method:'get'
    })    
}

const url_supply_chain='/routes/simple_api/supply_chain'
export function get_supply_chain(){
    return request({
        url:url_supply_chain,
        method:'get'
    })    
}

export function getGraphSidebarOptions(){
    return request({
        url:'/routes/simple_api/sidebar_options',
        method:'get'
    })
}

const url_insert_nodes='/routes/simple_api/insert_nodes'
export function insert_nodes(payload){
    return request({
        url:url_insert_nodes,
        method:'post',
        data: payload
    })    
}

const url_insert_links='/routes/simple_api/insert_links'
export function insert_links(payload){
    return request({
        url:url_insert_links,
        method:'post',
        data: payload
    })    
}
