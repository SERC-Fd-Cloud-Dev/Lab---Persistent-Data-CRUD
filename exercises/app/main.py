from fastapi import FastAPI, Depends, HTTPException, Response
from app.database import get_session
from app import repository
from app.schemas import EquipmentWrite, EquipmentRead

def create_app():
    app = FastAPI(title='Lab Equipment Register')
    app.state.equipment_cache = {}  # Add cache-aside behaviour in 6.4.

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.post('/equipment', status_code=201, response_model=EquipmentRead)
    def create(data: EquipmentWrite, session=Depends(get_session)):
        return repository.create_equipment(session, data.model_dump())

    @app.get('/equipment', response_model=list[EquipmentRead])
    def all_equipment(session=Depends(get_session)):
        return repository.list_equipment(session)

    @app.get('/equipment/{equipment_id}', response_model=EquipmentRead)
    def one(equipment_id: int, response: Response, session=Depends(get_session)):
        # TODO K1: look up the integer key in app.state.equipment_cache.
        item = repository.get_equipment(session, equipment_id)
        if item is None:
            raise HTTPException(404, 'Equipment not found')
        data = EquipmentRead.model_validate(item).model_dump()
        # TODO K2: cache this plain dictionary, set X-Cache to miss/hit.
        return data

    @app.put('/equipment/{equipment_id}', response_model=EquipmentRead)
    def replace(equipment_id: int, data: EquipmentWrite, session=Depends(get_session)):
        raise NotImplementedError('C3: call repository, handle missing record and return it')

    @app.delete('/equipment/{equipment_id}', status_code=204)
    def remove(equipment_id: int, session=Depends(get_session)):
        raise NotImplementedError('C4: delete or return 404; success has no response body')

    return app

app = create_app()
