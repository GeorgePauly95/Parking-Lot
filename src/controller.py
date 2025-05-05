from flask import request
from src.model import show_all_slots, show_ticket_details, update_parking_details, new_parking

def register_routes(app):
    @app.route('/api/slots')
    def show_all_slots_route():
        print("is the route being called?")
        return show_all_slots()

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