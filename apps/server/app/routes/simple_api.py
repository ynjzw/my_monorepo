from fastapi import FastAPI,Depends,APIRouter
from sqlalchemy.orm import Session
from database import get_db,engine
from models import Nodes,UploadFileRecord, ImportedData,Link,family,world,Structure,Population


app=APIRouter()
@app.get('/data')
def get_datas(db:Session=Depends(get_db)):
    data = db.query(ImportedData).all()
    return [item.to_dict() for item in data]

@app.get('/nodes')
def get_nodes(db:Session=Depends(get_db)):
    nodes = db.query(Nodes).all()
    return nodes

@app.get('/population_structure')
def get_population_structure(db:Session=Depends(get_db)):
    data = db.query(Population).all()
    return data

@app.get('/base_nodes')
def get_base_nodes(db:Session=Depends(get_db)):
    data = db.query(Nodes).filter(Nodes.type=='基础需求').all()
    return data

@app.get('/maslow_needs')
def get_maslow_needs(db:Session=Depends(get_db)):
    data = db.query(Nodes).filter(Nodes.type=='马斯洛需求').all()
    return data

@app.get('/old_structure')
def get_old_structure(db:Session=Depends(get_db)):
    data = db.query(Structure).filter(Structure.type=='old').all()
    return data

@app.get('/new_structure')
def get_new_structure(db:Session=Depends(get_db)):
    data = db.query(Structure).filter(Structure.type=='new').all()
    return data

@app.get('/link')
def get_link(db:Session=Depends(get_db)):
    link = db.query(Link).all()
    return link

@app.get('/solar')
def get_solar(db:Session=Depends(get_db)):
    solar = db.query(solar).all()
    return solar

@app.get('/family')
def get_family(db:Session=Depends(get_db)):
    data = db.query(family).all()
    return data

@app.get('/world')
def get_world(db:Session=Depends(get_db)):
    data = db.query(world).all()
    return data
