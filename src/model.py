import os, psycopg

conn = psycopg.connect(host=os.getenv("PL_HOST"),
                       dbname=os.getenv("PL_DBNAME"),
                       user=os.getenv("PL_USERNAME"),
                       password=os.getenv("PL_PASSWORD"))

def new_parking(number_plate, car_make, car_color):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT slot_number,floor_number FROM slots "
            "WHERE slot_number NOT IN (select slotid FROM tickets WHERE exit_time IS NULL) ORDER BY slots.slot_number ASC LIMIT 1;")
        slot_available = cur.fetchone()
        cur.execute("""INSERT INTO tickets(number_plate, car_make, car_color, slotid) VALUES(%s, %s, %s, %s)
                    RETURNING ticketid""",
                    (number_plate, car_make, car_color, slot_available[0]))
        created_ticketid=cur.fetchone()
        cur.execute("""
                    SELECT tickets.ticketid, tickets.entry_time, slots.slot_number, slots.floor_number FROM tickets
                    LEFT OUTER JOIN slots on tickets.slotid=slots.slot_number
                    WHERE tickets.ticketid=(%s);
                    """,created_ticketid)
        new_parking_details = cur.fetchone()
        conn.commit()
        return {
            "ticketid": new_parking_details[0],
            "entry_time": new_parking_details[1],
            "slot_number": new_parking_details[2],
            "floor_number": new_parking_details[3]
        }
def show_ticket_details(ticketid):
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT tickets.ticketid, tickets.number_plate, tickets.car_make, tickets.car_color,
                    tickets.entry_time,tickets.exit_time, slots.slot_number, slots.floor_number FROM tickets
                    LEFT OUTER JOIN slots ON tickets.slotid=slots.slot_number
                    WHERE ticketid=(%s)
                    """, (ticketid,))
        ticket_details = cur.fetchone()
        conn.commit()
        if ticket_details is None:
            return {"message": "Invalid ticketid"}
        else:
            return {
                "ticketid": ticket_details[0],
                "number_plate": ticket_details[1],
                "car_make": ticket_details[2],
                "car_color": ticket_details[3],
                "entry_time": ticket_details[4],
                "exit_time": ticket_details[5],
                "slot_number": ticket_details[6],
                "floor_number": ticket_details[7]
            }

def update_exit_time(ticketid):
    with conn.cursor() as cur:
        cur.execute("SELECT exit_time FROM tickets WHERE ticketid=(%s)",(ticketid,))
        exit_time = cur.fetchone()
        if exit_time is None:
            return {"message": "Invalid ticketid"}
        elif exit_time[0] is None:
            cur.execute("UPDATE tickets SET exit_time=CURRENT_TIMESTAMP, parking_charge=ROUND((EXTRACT(EPOCH FROM AGE(CURRENT_TIMESTAMP,entry_time))*50)/3600,4) WHERE ticketid = (%s)",(ticketid,))
            cur.execute(f"""
                        SELECT tickets.ticketid, tickets.number_plate, tickets.car_make, tickets.car_color,
                        tickets.entry_time,tickets.exit_time, tickets.parking_charge, slots.slot_number, slots.floor_number FROM tickets
                        LEFT OUTER JOIN slots ON tickets.slotid=slots.slot_number
                        WHERE ticketid = (%s)
                        """,(ticketid,))
            ticket_details = cur.fetchone()
            conn.commit()
            return {
                "ticketid": ticket_details[0],
                "number_plate": ticket_details[1],
                "car_make": ticket_details[2],
                "car_color": ticket_details[3],
                "entry_time": ticket_details[4],
                "exit_time": ticket_details[5],
                "parking_charge": ticket_details[6],
                "slot_number": ticket_details[7],
                "floor_number": ticket_details[8]
            }
        return {"message": "This ticket is already closed!"}

def show_location(number_plate):
    with conn.cursor() as cur:
        cur.execute(f"SELECT slots.slot_number, slots.floor_number from tickets LEFT OUTER JOIN slots ON slots.slot_number=tickets.slotid WHERE tickets.number_plate='{number_plate}' AND tickets.exit_time IS NULL")
        location = cur.fetchone()
        return {"slot_number": location[0], "floor_number": location[1]}

def show_all_slots():
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT slots.slot_number, slots.floor_number, open_tickets.number_plate, open_tickets.car_make, open_tickets.car_color
                    FROM slots
                    LEFT OUTER JOIN (SELECT tickets.number_plate, tickets.car_make, tickets.car_color, tickets.exit_time, tickets.slotid
                    FROM tickets WHERE tickets.exit_time IS NULL) AS open_tickets
                    ON slots.slot_number=open_tickets.slotid;
                    """)
        all_slots = cur.fetchall()
        conn.commit()
    return [
        {
            "slot_number": slot[0],
            "floor_number": slot[1],
            "car": None
        }
        if (slot[2] and slot[3] and slot[4]) is None

        else {
            "slot_number": slot[0],
            "floor_number": slot[1],
            "car": {"number_plate": slot[2],
                    "car_make": slot[3],
                    "car_color": slot[4]
                    }
        }
        for slot in all_slots
    ]

def show_number_plates(car_color, car_make):
    with conn.cursor() as cur:
        if car_color is None:
            cur.execute("""SELECT tickets.ticketid, tickets.number_plate, tickets.car_make, tickets.car_color, slots.slot_number, slots.floor_number
                                    FROM tickets
                                    LEFT OUTER JOIN slots ON slots.slot_number=tickets.slotid
                                    WHERE tickets.car_make=(%s) AND tickets.exit_time IS NULL""",(car_make,))
        elif car_make is None:
            cur.execute("""SELECT tickets.ticketid, tickets.number_plate, tickets.car_make, tickets.car_color, slots.slot_number, slots.floor_number
                                    FROM tickets
                                    LEFT OUTER JOIN slots ON slots.slot_number=tickets.slotid
                                    WHERE tickets.car_color=(%s) AND tickets.exit_time IS NULL""",(car_color,))
        else:
            cur.execute(f"""SELECT tickets.ticketid, tickets.number_plate, tickets.car_make, tickets.car_color, slots.slot_number, slots.floor_number
                        FROM tickets
                        LEFT OUTER JOIN slots ON slots.slot_number=tickets.slotid
                        WHERE tickets.car_color=(%s) AND tickets.car_make=(%s) AND tickets.exit_time IS NULL""",(car_color, car_make))
        number_plates = cur.fetchall()
        conn.commit()
        return [{"ticketid": number_plate[0],
                "number_plate": number_plate[1],
                "car_make": number_plate[2],
                "car_color": number_plate[3],
                "slot_number": number_plate[4],
                "floor_number": number_plate[5]} for number_plate in number_plates]