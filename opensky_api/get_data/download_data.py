from pyopensky.trino import Trino
from datetime import datetime
trino = Trino()

start = 1699276083 
end = 1699276083+(3600*1) 

history = trino.history(start=start,stop=end, arrival_airport='EHAM',bounds=(2,49,8,54))

history.to_csv('flights_sample_24_hours.csv')