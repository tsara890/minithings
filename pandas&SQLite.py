# Import module 
import sqlite3
import pandas


# Task 1: Create connection object
con = sqlite3.connect("hotel_booking.db")
 

# Task 2: Create cursor object
cur = con.cursor()


# Task 3: View first row of booking_summary
first_row = cur.execute("""SELECT * FROM booking_summary""").fetchone()

# Task 4: View first ten rows of booking_summary 
first_ten_rows = cur.execute("""SELECT * FROM booking_summary""").fetchmany(10)


# Task 5: Create object bra and print first 5 rows to view data
bra = cur.execute("""SELECT * FROM booking_summary WHERE country = "BRA";""").fetchall()


# Task 6: Create new table called bra_customers
cur.execute("""CREATE TABLE IF NOT EXISTS bra_customers(
  num INTEGER,
  hotel TEXT,
  is_cancelled INTEGER,
  lead_time INTEGER,
  arrival_date_year INTEGER,
  arrival_date_month TEXT,
  arrival_date_day_of_month INTEGER,
  adults INTEGER,
  children INTEGER,
  country TEXT,
  adr REAL,
  special_requests INTEGER
)""")



# Task 7: Insert the object bra into the table bra_customers
cur.executemany("""INSERT INTO bra_customers VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""", bra)


# Task 8: View the first 10 rows of bra_customers
first_ten = cur.execute("""SELECT * FROM bra_customers""").fetchmany(10)


# Task 9: Retrieve lead_time rows where the bookings were canceled

#lead_time_can = cur.execute("""SELECT * FROM bra_customers WHERE is_cancelled = 1;""").fetchall()

df = pandas.read_sql_query("""SELECT * FROM bra_customers; """, con)

#print(df.head(10))

bookings_cancelled = df[df["is_cancelled"] == 1]



# Task 10: Find average lead time for those who canceled and print results
avg_lead_time = round(bookings_cancelled["lead_time"].mean(), 2)
print(avg_lead_time)


# Task 11: Retrieve lead_time rows where the bookings were not canceled
bookings_not_cancelled = df[df["is_cancelled"] == 0]


# Task 12: Find average lead time for those who did not cancel and print results
avg_lead_time_not_can = round(bookings_not_cancelled["lead_time"].mean(), 2)
print(avg_lead_time_not_can)


# Task 13: Retrieve special_requests rows where the bookings were canceled
special_requests_cancelled = bookings_cancelled[bookings_cancelled["special_requests"] != 0]
#print(special_requests_cancelled)


# Task 14: Find total speacial requests for those who canceled and print results
total_special_requests_cancelled = special_requests_cancelled["special_requests"].sum()
print(total_special_requests_cancelled)



# Task 15: Retrieve special_requests rows where the bookings were not canceled
special_requests = bookings_not_cancelled[bookings_not_cancelled["special_requests"] != 0]


# Task 16: Find total speacial requests for those who did not cancel and print results
total_special_requests = special_requests["special_requests"].sum()
print(total_special_requests)

con.commit()
con.close()

