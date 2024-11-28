from pyopensky.trino import Trino

def download_data(start, stop, arrival_airport='EHAM', bounds=(2,49,8,54), save=False, file_name=None):
    trino = Trino()
    if file_name == None:
        file_name = f'{start}_{stop}_{arrival_airport}.csv'
    
    history = trino.history(start=start, stop=stop, arrival_airport=arrival_airport, bounds=bounds)

    if save:
        history.to_csv(file_name)

    return history

