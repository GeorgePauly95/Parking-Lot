# Parking lot API contracts

## 1. Create a parking entry
### Description:  This api creates a new parking entry and gives the user details about their parking
### Request:

#### Endpoint: POST /tickets
#### Body:
```
{
    "number_plate": "KA 53 BH 1234",
    "car_make": "Hyundai",
    "car_color" "Black" 
}
```
### Success Response:
#### Status: 201 Created
#### Body:
```
{
   "ticketid": 999876567111,
   "entry_time": 2025-04-23 12:45:00,
   "slot_number": 20,
   "floor_number": 1
}
```

## 2. Get parking details
### Description: This api retrieves information about the user's parking. Depending on when the information
### is requested, exit time and parking charge may be null. 
### Request:

#### Endpoint: GET /tickets/:ticketid
### Success Response:
#### Status: 200 ok
#### Body:
```json
{
    "ticketid": 999876567111,
    "number_plate": "KA 53 BH 1234",
    "car_make": "Hyundai",
    "car_color": "Black",
    "slot_number": 20,
    "floor_number": 1,
    "entry_time": 2025-04-23 12:45:00,
    "exit_time": 2025-04-23 17:05:00,
    "parking_charge":  100
}
```
### Error Response:
#### Status: 404 Not Found
#### Body:
```
{
    "message": "Invalid ticketid"
}
```
## 3. Update slot availability
### Description: This api updates the availability of a particular slot, and retrieves its parking details.
### Request:
#### Body:
```
{
    "status": "closed"
}
```

#### Endpoint: PATCH /tickets/:ticketid
### Success Response:
#### Status: 200 ok
#### Body:
```
{
    "ticketid": 999876567111,
    "number_plate": "KA 53 BH 1234",
    "car_make": "Hyundai",
    "car_color": "Black",
    "slot_number": 20,
    "floor_number": 1,
    "entry_time": 2025-04-23 12:45:00,
    "exit_time": 2025-04-23 17:05:00,
    "parking_charge":  100
}
```
### Error Response 1:
#### Status: 404 Not Found
#### Body:
```
{
    "message": "Invalid ticketid"
}
```
### Error Response 2:
#### Status: 409 Conflict
#### Body:
```
{
    "message": "This ticket is already closed!"
}
```
## 4. Show slot availability
### Description: Provides availability or lack thereof of all slots in the parking lot
### Request:

#### Endpoint: GET /slots
### Success Response:
#### Status: 200 ok
#### Body:
```
[   
    {"slot_id": 1,
     "floor_number": 1,
     "car": null
     },
    
    {
    "slot_id": 2
    "floor_number": 1,
    "car": {
             "number_plate": "KA 03 BH 7778" ,
             "car_make": "Honda",
             "car_color: "White"
           }
    } , 
    
    ...
    
    {"slot_id": 100,
     "floor_number": 5,
     "car": null
    }
]
```
### Error Response:
#### Status: 500 Internal Server Error

## 5. Show car number plates
### Description: Get number plates of cars of a particular color
### Request:
#### Endpoint: Get /tickets?car-color=Red

### Success Response:
#### Status: 200 ok
#### Body:
```
[
    {
     "number_plate": KA 01 AB 1024 ,
     "slot_number": 23,
     "floor_number": 1
    },
    
    {
     "number_plate": KA 01 GH 0256,
     "slot_number": 26,
     "floor_number": 2
    },
    
    {
     "number_plate": KA 01 XX 2048,
     "slot_number": 29,
     "floor_number": 2
    }
]
```

## 6. Show car location
### Description: Get location of a car with a particular number plate
### Request:
#### Endpoint: Get /slots?number-plate=KA01BH1024

### Success Response:
#### Status: 200 ok
#### Body:
```
{
    "slot_number": 23,
    "floor_number": 1
}