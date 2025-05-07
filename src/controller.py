from flask import request

from src.model import show_all_slots, show_ticket_details, update_exit_time, new_parking, show_number_plates, show_location

def register_routes(app):

    #4th and 6th APIs
    @app.route('/api/slots')
    def show_location_route():
        if request.args.get("number-plate") is None:
            if show_all_slots() is None:
                return """<title>500 Internal Server Error</title>
                        </head><body><h1>Internal Server Error</h1>
                        <p>The server was unable to complete your request. Please try again later.</p>""", 500
            return show_all_slots(), 200, {"Access-Control-Allow-Origin":"*"}
        else:
            number_plate = request.args.get("number-plate")
            return show_location(number_plate), 200, {"Access-Control-Allow-Origin":"*"}

    #1st API
    @app.route('/api/tickets', methods=['POST'])
    def new_parking_route():
        new_parking_details = request.get_json()
        number_plate=new_parking_details["number_plate"]
        car_make=new_parking_details["car_make"]
        car_color=new_parking_details["car_color"]
        return new_parking(number_plate, car_make, car_color)

    # 2nd API
    @app.route('/api/tickets/<int:ticketid>')
    def show_parking_details(ticketid):
        ticket_details = show_ticket_details(ticketid)
        if ticket_details == {"message": "Invalid ticketid"}:
            return {"message": "Invalid ticketid"}, 404
        return ticket_details

    #3rd API
    @app.route('/api/tickets/<int:ticketid>', methods=['PATCH'])
    def update_parking(ticketid):
        ticket_closure = request.get_json()
        if ticket_closure["status"] == "closed":
            ticket_status = update_exit_time(ticketid)
            if ticket_status == {"message": "Invalid ticketid"}:
                return {"message": "Invalid ticketid"}, 404
            elif ticket_status == {"message": "This ticket is already closed!"}:
                return {"message": "This ticket is already closed!"}, 409
            else:
                return ticket_status

    #5th API
    @app.route('/api/tickets')
    def show_number_plates_route():
        color = request.args.get("car-color")
        make = request.args.get("car-make")
        return show_number_plates(color, make)