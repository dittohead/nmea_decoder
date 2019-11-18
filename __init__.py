# http://aprs.gids.nl/nmea/
# https://docs.novatel.com/OEM7/Content/Logs/GPGGA.htm
# https://docs.novatel.com/OEM7/Content/Logs/GPRMC.htm

def nmea_decode(str, raw=True):
    try:
        _calc_checksum(str)
        msg = str.split(',')
        if msg[0]=='$GPGGA':
            result = _decode_gpgga(msg, raw)
        elif msg[0]=='$GPRMC':
            result = _decode_gprmc(msg, raw)
        return result

    except ValueError:
            return {"error": "checksum mismatch"}


def _decode_gpgga(list, raw):
    result = {}
    gpgga_keys = [
        "tag",
        "utc",
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

    checksum = list.pop()
    dif, checksum = checksum.split('*')
    list.append(dif)
    list.append(checksum)
    result = dict(zip(gpgga_keys, list))
    lat = _calc_lat(result['lat'], result['lat_dir'])
    lon = _calc_lon(result['lon'], result['lon_dir'])
    result.update({"lat": lat})
    result.update({"lon": lon})
    if raw:
        return result
    else:
        _result = {}
        for item in result:
            if result[item]!='':
                _result.update({item: result[item]})
        return _result


def _decode_gprmc(list, raw):
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
    checksum = list.pop()
    mode_ind, checksum = checksum.split('*')
    list.append(mode_ind)
    list.append(checksum)
    result = dict(zip(gprmc_keys, list))
    lat = _calc_lat(result['lat'], result['lat_dir'])
    lon = _calc_lon(result['lon'], result['lon_dir'])
    result.update({"lat": lat})
    result.update({"lon": lon})
    if raw:
        return result
    else:
        _result = {}
        for item in result:
            if result[item]!='':
                _result.update({item: result[item]})
        return _result


def _calc_checksum(str):
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


def _bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result


def _calc_lat(lat, ns):
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
    
#todo add timestamp fix