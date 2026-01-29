
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

const url4='/test1'
export function getAIRes(data){
    return request.post(
        url4,
        {'data':data}
    )    
}

const url5='https://echarts.apache.org/examples/data/asset/data/option-view.json'
export async function getJson(){
    try {
    // 方案1: 使用本地代理
    const response = await axios.get('/api/proxy/echarts-data', {
      params: {
        url: 'https://echarts.apache.org/examples/data/asset/data/option-view.json'
      }
    });
    return response.data;
  } catch (error) {
    console.error('获取数据失败:', error);
    throw error;
  }   
}

const url6='/family'
export function getFamily(){
    return request({
        url:url6,
        method:'get'
    })    
}

const url7='https://echarts.apache.org/zh/js/vendors/d3-hierarchy@2.0.0/dist/d3-hierarchy.min.js'
export function getJs(){
    return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = url7;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  }); 
}