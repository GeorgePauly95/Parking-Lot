import psycopg, os


conn = psycopg.connect(host=os.getenv("PL_HOST"),
                       dbname=os.getenv("PL_DBNAME"),
                       user=os.getenv("PL_USERNAME"),
                       password=os.getenv("PL_PASSWORD"))

# conn = psycopg.connect(os.getenv("RENDER_DATABASE_URL"))

cur = conn.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS slots(
            slot_number integer PRIMARY KEY,
            floor_number integer
            );            
            """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets(
            ticketid bigserial PRIMARY KEY,
            number_plate text,
            car_make text,
            car_color text,
            entry_time timestamp without time zone DEFAULT NOW(),
            exit_time timestamp without time zone,
            parking_charge integer,
            slotid integer,
            CONSTRAINT fk_slots
            FOREIGN KEY(slotid) REFERENCES slots(slot_number)
            );
            """)

#manually inserting data
slots = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 1), (10, 1),
         (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1), (17, 1), (18, 1), (19, 1), (20, 1),
         (21, 1), (22, 1), (23, 1), (24, 1), (25, 2), (26, 2), (27, 2), (28, 2), (29, 2), (30, 2),
         (31,2), (32,2), (33,2), (34,2), (35,2), (36,2), (37,2), (38,2), (39,2), (40,2), (41,3),
         (42,3), (43,3), (44,3), (45,3), (46,3), (47,3), (48,3), (49,3), (50,3), (51,3), (52, 3),
         (53,3), (54,3), (55,3), (56,3)]

# floor_arr = [0, 1, 2, 3]
# slots_arr = [8, 16, 16, 16]
# for n in range(1,56):
#     (n,floor_arr[0])



for x in slots:
    cur.execute(f"""INSERT INTO slots (slot_number, floor_number)
    VALUES {x}
    ON CONFLICT (slot_number)
    DO NOTHING;""")

conn.commit()
cur.close()
conn.close()