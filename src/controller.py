from flask import request


from src.model import show_all_slots, show_ticket_details, update_exit_time, new_parking, show_number_plates, show_location

def register_routes(app):
    @app.route('/api/slots')
    def show_location_route():
        if request.args.get("number-plate") is None:
            try:
                all_slots = show_all_slots()
                if not all_slots:
                    return """<title>500 Internal Server Error</title>
                            </head><body><h1>Internal Server Error</h1>
                            <p>The server was unable to complete your request. Please try again later.</p>""", 500
                return all_slots, 200, {"Access-Control-Allow-Origin":"*"}
            except psycopg.errors.UndefinedTable:
                return """<title>500 Internal Server Error</title>
                        </head><body><h1>Internal Server Error</h1>
                        <p>The server was unable to complete your request. Please try again later.</p>""", 500
        else:
            number_plate = request.args.get("number-plate")
            return show_location(number_plate), 200, {"Access-Control-Allow-Origin":"*"}

    @app.route('/api/tickets', methods=['POST'])
    def new_parking_route():
        new_parking_details = request.get_json()
        number_plate=new_parking_details["number_plate"]
        car_make=new_parking_details["car_make"]
        car_color=new_parking_details["car_color"]
        return new_parking(number_plate, car_make, car_color), 200, {"Access-Control-Allow-Origin":"*"}

    @app.route('/api/tickets/<int:ticketid>')
    def show_parking_details(ticketid):
        ticket_details = show_ticket_details(ticketid)
        if ticket_details == {"message": "Invalid ticketid"}:
            return {"message": "Invalid ticketid"}, 404
        return ticket_details, 200, {"Access-Control-Allow-Origin":"*"}

    @app.route('/api/tickets/<int:ticketid>', methods=['PATCH'])
    def update_parking(ticketid):
        ticket_closure = request.get_json()
        try:
            if ticket_closure["status"] == "closed":
                ticket_status = update_exit_time(ticketid)
                if ticket_status == {"message": "Invalid ticketid"}:
                    return {"message": "Invalid ticketid"}, 404
                elif ticket_status == {"message": "This ticket is already closed!"}:
                    return {"message": "This ticket is already closed!"}, 409
                return ticket_status, 200, {"Access-Control-Allow-Origin":"*", "Access-Control-Allow-Methods":"*"}
        except KeyError:
            return 'Bad Request', 400

    @app.route('/api/tickets')
    def show_number_plates_route():
        color = request.args.get("car-color")
        make = request.args.get("car-make")
        return show_number_plates(color, make), 200, {"Access-Control-Allow-Origin":"*"}