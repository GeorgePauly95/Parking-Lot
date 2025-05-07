import psycopg, os

conn = psycopg.connect(host=os.getenv("PL_HOST"),
                       dbname=os.getenv("PL_DBNAME"),
                       user=os.getenv("PL_USERNAME"),
                       password=os.getenv("PL_PASSWORD"))

# conn = psycopg.connect(os.getenv("RENDER_DATABASE_URL"))

cur = conn.cursor()

# cur.execute("""CREATE SEQUENCE IF NOT EXISTS slot AS integer INCREMENT 1 MINVALUE 1 MAXVALUE 72 START 57;
#             CREATE TABLE IF NOT EXISTS slots(slot_number integer DEFAULT NEXTVAL('slot') PRIMARY KEY,floor_number integer);
#             INSERT INTO slots(floor_number) SELECT 0 FROM generate_series(1,8) ON CONFLICT DO NOTHING;
#             INSERT INTO slots(floor_number) SELECT 1 FROM generate_series(1,16) ON CONFLICT DO NOTHING;
#             INSERT INTO slots(floor_number) SELECT 2 FROM generate_series(1,16) ON CONFLICT DO NOTHING;
#             INSERT INTO slots(floor_number) SELECT 3 FROM generate_series(1,16) ON CONFLICT DO NOTHING;
#             INSERT INTO slots(floor_number) SELECT 4 FROM generate_series(1,16) ON CONFLICT DO NOTHING;
#             CREATE TABLE IF NOT EXISTS tickets(
#             ticketid bigserial PRIMARY KEY,
#             number_plate text,
#             car_make text,
#             car_color text,
#             entry_time timestamp without time zone DEFAULT NOW(),
#             exit_time timestamp without time zone,
#             parking_charge integer,
#             slotid integer,
#             CONSTRAINT fk_slots
#             FOREIGN KEY(slotid) REFERENCES slots(slot_number)
#             );""")

cur.execute("""CREATE TABLE IF NOT EXISTS slots(slot_number integer PRIMARY KEY,floor_number integer);
            INSERT INTO slots(slot_number) VALUES (generate_series(1,56)) ON CONFLICT DO NOTHING;
            UPDATE slots SET floor_number=0 from generate_series(1,8) WHERE slot_number<=8;
            UPDATE slots SET floor_number=1 from generate_series(1,16) WHERE slot_number<=24 AND slot_number >8;
            UPDATE slots SET floor_number=2 from generate_series(1,16) WHERE slot_number<=40 AND slot_number >16;
            UPDATE slots SET floor_number=3 from generate_series(1,16) WHERE slot_number<=56 AND slot_number >40;
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
            );""")

conn.commit()
cur.close()
conn.close()