from tools.extract_state_info import extract_state_info
import pandas as pd
import numpy as np

def angle_difference(angle1, angle2):
    diff = (angle2 - angle1 + 180) % 360 - 180
    return diff

def kwikqdrdist(lata, lona, latb, lonb):
    """Gives quick and dirty qdr[deg] and dist [m]
       from lat/lon. (note: does not work well close to poles)"""

    re      = 6371000.  # radius earth [m]
    dlat    = np.radians(latb - lata)
    dlon    = np.radians(((lonb - lona)+180)%360-180)
    cavelat = np.cos(np.radians(lata + latb) * 0.5)

    dangle  = np.sqrt(dlat * dlat + dlon * dlon * cavelat * cavelat)
    dist    = re * dangle

    qdr     = np.degrees(np.arctan2(dlon * cavelat, dlat)) % 360.

    return qdr, dist

def estimate_runway(traffic, takeoff=False, landing=True, summary=None):
    if summary is None:
        summary = traffic.summary(['icao24','callsign']).eval()
    if landing:
        return estimate_landing_runway(traffic,summary)
    if takeoff:
        return estimate_takeoff_runway(traffic,summary)
    
def estimate_takeoff_runway(traffic, summary):
    print('Estimating take-off runway not yet implemented')
    return summary

def estimate_landing_runway(traffic, summary):
    # maybe first get final track and position
    # then compute loss w.r.t. track, positions and bearing of all rwys, assign one with lowest loss
    # raise warning or something if all losses big
    runways_schiphol = {
        "18C": {"lat": 52.301851, "lon": 4.737557, "track": 183},
        "36C": {"lat": 52.330937, "lon": 4.740026, "track": 3},
        "18L": {"lat": 52.291274, "lon": 4.777391, "track": 183},
        "36R": {"lat": 52.321199, "lon": 4.780119, "track": 3},
        "18R": {"lat": 52.329170, "lon": 4.708888, "track": 183},
        "36L": {"lat": 52.362334, "lon": 4.711910, "track": 3},
        "06":   {"lat": 52.304278, "lon": 4.776817, "track": 60},
        "24":   {"lat": 52.288020, "lon": 4.734463, "track": 240},
        "09":   {"lat": 52.318362, "lon": 4.796749, "track": 87},
        "27":   {"lat": 52.315940, "lon": 4.712981, "track": 267},
        "04":   {"lat": 52.313783, "lon": 4.802666, "track": 45},
        "22":   {"lat": 52.300518, "lon": 4.783853, "track": 225}
    }

    if 'track_term' not in summary:
        summary = extract_state_info(traffic, summary)

    summary['runway'] = None
    summary['runway_loss'] = 10000

    for flight in traffic:
        loss = 100000
        runway = None
        lat_mean = flight.last(200).data.latitude
        lon_mean = flight.last(200).data.longitude
        track_mean = flight.last(200).data.track
        for rwy, rwy_info in runways_schiphol.items():
            qdr, dist = kwikqdrdist(lat_mean, lon_mean, rwy_info['lat'], rwy_info['lon'])
            loss_rwy = abs(angle_difference(qdr,track_mean)).mean() + abs(angle_difference(track_mean,rwy_info['track'])).mean() + (0.00000001*dist**2).mean()
            if loss_rwy < loss:
                loss = loss_rwy
                runway = rwy

        summary.loc[(summary['icao24'] == flight.icao24) & (summary['callsign'] == flight.callsign), ['runway','runway_loss']] = [runway,loss]
    
    return summary
