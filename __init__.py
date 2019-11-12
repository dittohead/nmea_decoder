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
    list.remove('$GPGGA')
    gpgga_keys = [
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
    if raw:
        result = dict(zip(gpgga_keys, list))
    else:
        _result = dict(zip(gpgga_keys, list))
        for item in _result:
            if _result[item] != '':
                result.update({item: _result[item]})

    return result


def _decode_gprmc(list, raw):
    result = {}
    list.remove('$GPRMC')
    gprmc_keys = [
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
    if raw:
        result = dict(zip(gprmc_keys, list))
    else:
        _result = dict(zip(gprmc_keys, list))
        for item in _result:
            if _result[item]!='':
                result.update({item: _result[item]})

    return result


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