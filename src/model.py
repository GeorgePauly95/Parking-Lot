import os, psycopg

conn = psycopg.connect(host=os.getenv("PL_HOST"),
                       dbname=os.getenv("PL_DBNAME"),
                       user=os.getenv("PL_USERNAME"),
                       password=os.getenv("PL_PASSWORD"))


def new_parking(number_plate, car_make, car_color):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT slot_number,floor_number FROM slots "
            "WHERE slot_number NOT IN (select slotid FROM tickets WHERE exit_time IS NULL) ORDER BY slots.slot_number ASC;")
        slot_available = cur.fetchone()
        cur.execute("INSERT INTO tickets(number_plate, car_make, car_color, slotid) VALUES(%s, %s, %s, %s)",
                    (number_plate, car_make, car_color, slot_available[0]))
        cur.execute(f"""
                    SELECT tickets.ticketid, tickets.entry_time, slots.slot_number, slots.floor_number FROM tickets
                    LEFT OUTER JOIN slots on tickets.slotid=slots.slot_number
                    ORDER BY tickets.ticketid DESC LIMIT 1;
                    """)
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
        #use prepared statements
        cur.execute(f"""
                    SELECT tickets.ticketid, tickets.number_plate, tickets.car_make, tickets.car_color,
                    tickets.entry_time,tickets.exit_time, slots.slot_number, slots.floor_number FROM tickets
                    LEFT OUTER JOIN slots ON tickets.slotid=slots.slot_number
                    WHERE ticketid={ticketid}
                    """)
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


# change function name to specific
def update_parking_details(ticketid):
    with conn.cursor() as cur:
        #use prepared statements

        cur.execute(f"SELECT exit_time FROM tickets WHERE ticketid={ticketid}")
        #change ticket_status to exit_time
        ticket_status = cur.fetchone()
        if ticket_status[0] is None:
            # use prepared statements

            cur.execute(f"UPDATE tickets SET exit_time=CURRENT_TIMESTAMP WHERE ticketid = {ticketid}")
#merge both Update statements
            cur.execute(
                f"UPDATE tickets SET parking_charge=ROUND((EXTRACT(EPOCH FROM AGE(exit_time,entry_time))*50)/3600,4) WHERE ticketid={ticketid}")

            cur.execute(f"""
                        SELECT tickets.ticketid, tickets.number_plate, tickets.car_make, tickets.car_color,
                        tickets.entry_time,tickets.exit_time, tickets.parking_charge, slots.slot_number, slots.floor_number FROM tickets
                        LEFT OUTER JOIN slots ON tickets.slotid=slots.slot_number
                        WHERE ticketid = {ticketid}
                        """)
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


def show_all_slots():
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT slots.slot_number, slots.floor_number, tickets.number_plate, tickets.car_make, tickets.car_color,tickets.exit_time
                    FROM slots
                    LEFT OUTER JOIN tickets ON slots.slot_number=tickets.slotid
                    ORDER BY slots.slot_number;
                    """)
        all_slots = cur.fetchall()
        conn.commit()
    return [
        {
            "slot_number": slot[0],
            "floor_number": slot[1],
            "car": None
        }
        if (slot[2] and slot[3] and slot[3]) is None

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
