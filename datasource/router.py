from fastapi import APIRouter, status, UploadFile, File
from fastapi.responses import JSONResponse

from . import controller

route = APIRouter(prefix='/data-source', tags=["data"])


@route.put('/upload-file')
async def upload_file(file: UploadFile = File()):
    data = await file.read()
    filename = file.filename
    new_items = await controller.create_item(data, filename)
    if not isinstance(new_items, Exception):
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={ "ids": new_items }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={ "message": "error while saving file" }
        )

@route.get('/list')
def list_files():
    all = controller.get_all()
    if len(all) > 0:    
        return all
    else:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT, 
            content=None
        )

@route.get('/get')
def get_item(id: str):
    item = controller.get_item(id)
    if not isinstance(item, Exception):
        return item
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={ type(item).__name__: str(item) }
        )

@route.delete('/delete')
def delete_item(id: str):
    if controller.delete_item(id):    
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=None
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content={"error": "Cannot delete"}
        )
        
        