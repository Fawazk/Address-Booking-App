from fastapi import HTTPException
from sqlalchemy.orm import Session
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from . import schemas,models




def fetch_location(street):
    """Fetching Address, Latitude and Longitude by street"""
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(street)
    return getLoc


def create_address(db: Session, address: schemas.FinalAddress):
    location = fetch_location(address.street)
    if location:
        address.address = str(location)
        list_of_addres = address.address.split(',')
        address.city = list_of_addres[1]
        address.latitude = str(location.latitude)
        address.longitude = str(location.longitude)
        Addressess = models.BookAddressess(**address.dict())
        db.add(Addressess)
        db.commit()
        db.refresh(Addressess)
        return Addressess
    else:
        raise HTTPException(
            status_code=404, detail="Pls enter a valid street name")



def get_coordinates(street_name):
    """return the given cities (latitude, longitude) tuple with location co-ordinates"""
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(street_name)
    return getLoc.latitude, getLoc.longitude



def calculate_distance(input_street: str, address_street: str):
    """by getting city names and returns the distance between the cities based on the location coordinates"""
    input_street = get_coordinates(input_street)
    address_street = get_coordinates(address_street)
    distance_difference = geodesic(input_street, address_street).km
    return distance_difference


def get_nearby_addresses(address_id: int, distance_in_km: int,input_address, db: Session):
    """By geting the address id and distance km we will filter and return the list of nearby addressess"""
    input_street = input_address.street
    all_addresses = db.query(models.BookAddressess).all()
    nearby_addresses = []
    for address in all_addresses:
        if address_id != address.id:
            calculated_distance = calculate_distance(input_street, address.street)
            """we got the difference b/w two cities which we given as parameter"""
            if calculated_distance < distance_in_km:
                nearby_addresses.append(address)
    return nearby_addresses


def edit_address(db:Session,address:schemas.FinalAddress,address_id:int):
    """To edit the address which filtered by given address id return the updated address"""
    db_address = db.get(models.BookAddressess,address_id)
    location = fetch_location(address.street)
    if location:
        address.address = str(location)
        list_of_addres = address.address.split(',')
        address.city = list_of_addres[1]
        address.latitude = str(location.latitude)
        address.longitude = str(location.longitude)
        address_data = address.dict(exclude_unset=True)
        for key, value in address_data.items():
            setattr(db_address,key,value)
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address
    else:
        raise HTTPException(
            status_code=404, detail="Pls enter a valid street name")