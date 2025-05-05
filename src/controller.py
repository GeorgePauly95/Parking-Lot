from flask import request
from src.model import show_all_slots, show_ticket_details, update_parking_details, new_parking, show_number_plates, show_location

def register_routes(app):

    @app.route('/api/slots')
    def show_location_route():
        if request.args.get("number-plate") is None:
            return show_all_slots()
        else:
            number_plate = request.args.get("number-plate")
            return show_location(number_plate)

    @app.route('/api/tickets', methods=['POST'])
    def new_parking_route():
        new_parking_details = request.get_json()
        number_plate=new_parking_details["number_plate"]
        car_make=new_parking_details["car_make"]
        car_color=new_parking_details["car_color"]
        return new_parking(number_plate, car_make, car_color)

    @app.route('/api/tickets/<int:ticketid>')
    def show_parking_details(ticketid):
        return show_ticket_details(ticketid)

    @app.route('/api/tickets/<int:ticketid>', methods=['PATCH'])
    def update_parking(ticketid):
        parking_query = request.get_json()
        if parking_query["status"] == "closed":
            return update_parking_details(ticketid)

    @app.route('/api/tickets')
    def show_number_plates_route():
        color = request.args.get("car-color")
        make = request.args.get("car-make")
        return show_number_plates(color, make)