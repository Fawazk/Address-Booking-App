from fastapi import FastAPI, Depends, HTTPException
from . import schemas, models, function
from .database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/add-address", response_model=schemas.FinalAddress)
def create_address(address: schemas.FirstAddress, db: Session = Depends(get_db)):
    """To add the address you want to add name and street feilds others are autogenerate"""
    return function.create_address(db=db, address=address)


@ app.get("/list-addresses/", response_model=list[schemas.FinalAddress])
def list_addresses(db: Session = Depends(get_db)):
    """This will return the all the addressess in database"""
    list_of_addresses = db.query(models.BookAddressess).all()
    return list_of_addresses


@ app.get("/list_nearby_addresses/")
def list_nearby_addresses(address_id: int, distance_km: int, db: Session = Depends(get_db)):
    """This will return a list of all the nearby addresses, within the given distance (km)"""
    input_address = db.query(models.BookAddressess).filter(
        models.BookAddressess.id == address_id).first()
    if input_address is None:
        raise HTTPException(
            status_code=404, detail="This address id is not found in our database . pls enter any correct address id")
    nearby_addresses_list = function.get_nearby_addresses(
        address_id, distance_km, input_address, db)
    return nearby_addresses_list


@app.delete("/delete-address/{address_id}/")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """Delete address filtered by address_id which you given"""
    address = db.get(models.BookAddressess, address_id)
    if address:
        db.delete(address)
        db.commit()
        return {"Is_deleted": True}
    else:
        raise HTTPException(
            status_code=404, detail="This address id is not found in our database . pls enter any correct address id")


@app.patch("/edit-address/{address_id}/", response_model=schemas.FinalAddress)
def edit_address(address: schemas.FirstAddress, address_id: int, db: Session = Depends(get_db)):
    """Fetching the address by address id which you given and returns edited address , you can update name feild and street feild"""
    db_address = db.get(models.BookAddressess, address_id)
    if not db_address:
        raise HTTPException(
            status_code=404, detail="This address id is not found in our database . pls enter any correct address id")
    return function.edit_address(db=db, address=address, address_id=address_id)
