# http://aprs.gids.nl/nmea/
# https://docs.novatel.com/OEM7/Content/Logs/GPGGA.htm
# https://docs.novatel.com/OEM7/Content/Logs/GPRMC.htm
import re


def nmea_decode(str, raw=True):
    """

    :param str: Raw GPS string $GPXXX[]
    :param raw: if true returns all value include empty
    :return: dict with keys
    """
    try:
        _calc_checksum(str)
        msg = str.split(',')
        if msg[0]=='$GPGGA':
            result = _decode_gpgga(msg, raw)
            return result
        elif msg[0]=='$GPRMC':
            result = _decode_gprmc(msg, raw)
            return result
        else:
            return {"error": "No decoder for " + msg[0] + " GPS data"}

    except ValueError:
        return {"error": "checksum mismatch"}

    except UnboundLocalError:
        raise


def _decode_gpgga(message_list, raw):
    result = {}
    gpgga_keys = [
        "tag",
        "utc_time_raw",
        "lat",
        "lat_dir",
        "lon",
        "lon_dir",
        "quality",
        "sattelite_num",
        "hdop",
        "altitude",
        "altitude_units",
        "geoidal_separation",
        "geoidal_separation_val",
        "age",
        "dif_reference",
        "checksum"
    ]

    checksum = message_list.pop()
    dif, checksum = checksum.split('*')
    message_list.append(dif)
    message_list.append(checksum)
    result = dict(zip(gpgga_keys, message_list))
    lat = _calc_lat(result['lat'], result['lat_dir'])
    lon = _calc_lon(result['lon'], result['lon_dir'])
    result.update({"lat": lat})
    result.update({"lon": lon})
    if raw:
        return result
    else:
        _result = {}
        for item in result:
            if result[item] != '':
                _result.update({item: result[item]})
        return _result


def _decode_gprmc(message_list, raw):
    result = {}
    gprmc_keys = [
        "tag",
        "utc",
        "pos_status",
        "lat",
        "lat_dir",
        "lon",
        "lon_dir",
        "speed_knots",
        "true_course",
        "date",
        "variation",
        "variation_dir",
        "mode_ind",
        "checksum"
    ]
    checksum = message_list.pop()
    mode_ind, checksum = checksum.split('*')
    message_list.append(mode_ind)
    message_list.append(checksum)
    result = dict(zip(gprmc_keys, message_list))
    lat = _calc_lat(result['lat'], result['lat_dir'])
    lon = _calc_lon(result['lon'], result['lon_dir'])
    result.update({"lat": lat})
    result.update({"lon": lon})
    timestamp = _calc_utc_timestamp(result['utc'], result['date'])
    result.update({"utc_timestamp": timestamp})
    result.pop('utc')
    result.pop('date')
    if raw:
        return result
    else:
        _result = {}
        for item in result:
            if result[item]!='':
                _result.update({item: result[item]})
        return _result


def _calc_checksum(str):
    """

    :param str: Raw GPS string
    :return: boolean, raise Value error
    """
    checksum = 0
    raw_string, str_checksum = str.split('*')
    str_checksum = int(str_checksum, 16)
    raw_string = raw_string.lstrip("$")
    for char in raw_string:
        checksum = checksum ^ (_bytes_to_int(char.encode()))
    if checksum == str_checksum:
        return True
    else:
        raise ValueError("Checksum mismath!")
        return False


def _bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result


def _calc_lat(lat, ns):
    """

    :param lat: Raw GPS latitude eg 4827.7740
    :param ns: North or South
    :return: xx.xxxxxx deg, -xx.xxxxxx if South
    """
    deg_min, sec = str(lat).split('.')
    deg = deg_min[0:2]
    deg = int(deg)
    min = int(deg_min[2:4])
    min_sec = str(min) + '.' + sec
    min_sec = float(min_sec)
    deg_part = min_sec / 60
    deg_part = float(format(deg_part, '.6f'))
    lat_deg = deg + deg_part
    if ns == "S" or ns == 's':
        lat_deg *= -1
    return lat_deg


def _calc_lon(lon, ew):
    """

    :param lon: Raw GPS longtitude eg 03503.3341
    :param ew: East or West
    :return:  yy.yyyyyy deg, -yy.yyyyyy if West
    """
    lon = lon.lstrip("0")
    deg_min, sec = str(lon).split('.')
    deg = deg_min[0:2]
    deg = int(deg)
    min = int(deg_min[2:4])
    min_sec = str(min) + '.' + sec
    min_sec = float(min_sec)
    deg_part = min_sec / 60
    deg_part = float(format(deg_part, '.6f'))
    lon_deg = deg + deg_part
    if ew == "W" or ew == 'w':
        lon_deg *= -1
    return lon_deg


def _calc_utc_timestamp(gps_time, gps_date):
    """
    by default years read from interval from 1950 to 2049
    :param gps_time: time from GPS string like HH.MM.SS.xxx
    :param gps_date: date from GPS string like ddmmyy
    :return: timestamp in UTC format yyyy-mm-ddTHH:MM:SSZ, in case of error return 1970-01-01T00:00:00Z
    """
    try:
        hms, msec = gps_time.split('.')
        hh, mm, ss = re.findall(r'\d\d', hms)
    except ValueError:
        hh = 00
        mm = 00
        ss = 00
    try:
        day, month, year = re.findall(r'\d\d', gps_date)
        year = int(year)
    except ValueError:
        day = 1
        month = 1
        year = 70

    if year < 49:
        year_full = 2000 + int(year)
    elif year > 50:
        year_full = 1900 + int(year)

    timestamp = '{yyyy}-{mm}-{dd}T{HH}:{MM}:{SS}Z'.format(yyyy=year_full, mm=month, dd=day, HH=hh, MM=mm, SS=ss)
    return timestamp
