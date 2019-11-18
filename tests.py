import unittest
import __init__ as nmea_decoder

class test_nmea(unittest.TestCase):
    def test_wrong_crc(self):
        gpgga_str = "$GPGGA,080633.000,4926.1601,N,03403.2484,W,1,05,5.1,86.0,M,,,,0000*3E"
        gprmc_str = "$GPRMC,080633.000,A,4923.1601,N,03605.2484,W,,,111119,,,A*68"

        a = nmea_decoder.nmea_decode(gpgga_str)
        self.assertEqual(a['error'], "checksum mismatch")

        b = nmea_decoder.nmea_decode(gprmc_str)
        self.assertEqual(b['error'], "checksum mismatch")


    def test_raw_parse(self):
        gpgga_str = "$GPGGA,080633.000,4827.1601,N,03503.2484,E,1,05,5.1,86.0,M,,,,0000*3E"
        gpgga_dict = {'tag': '$GPGGA',
                      'utc_time_raw': '080633.000',
                      'lat': 48.452668,
                      'lat_dir': 'N',
                      'lon': 35.05414,
                      'lon_dir': 'E',
                      'quality': '1',
                      'sattelite_num': '05',
                      'hdop': '5.1',
                      'altitude': '86.0',
                      'altitude_units': 'M',
                      'geoidal_separation': '',
                      'geoidal_separation_val': '',
                      'age': '',
                      'dif_reference': '0000',
                      'checksum': '3E'}
        gprmc_str = "$GPRMC,080633.000,A,4827.1601,N,03503.2484,E,,,111119,,,A*68"
        gprmc_dict = {'tag': '$GPRMC',
                      'pos_status': 'A',
                      'lat': 48.452668,
                      'lat_dir': 'N',
                      'lon': 35.05414,
                      'lon_dir': 'E',
                      'speed_knots': '',
                      'true_course': '',
                      'utc_timestamp': '2019-11-11T08:06:33Z',
                      'variation': '',
                      'variation_dir': '',
                      'mode_ind': 'A',
                      'checksum': '68'}

        a = nmea_decoder.nmea_decode(gpgga_str)
        self.assertEqual(a, gpgga_dict)

        b = nmea_decoder.nmea_decode(gprmc_str)
        self.assertEqual(b, gprmc_dict)


    def test_non_empty_vals(self):
        gpgga_str = "$GPGGA,080633.000,4827.1601,N,03503.2484,E,1,05,5.1,86.0,M,,,,0000*3E"
        gpgga_dict = {'tag': '$GPGGA',
                      'utc_time_raw': '080633.000',
                      'lat': 48.452668,
                      'lat_dir': 'N',
                      'lon': 35.05414,
                      'lon_dir': 'E',
                      'quality': '1',
                      'sattelite_num': '05',
                      'hdop': '5.1',
                      'altitude': '86.0',
                      'altitude_units': 'M',
                      'dif_reference': '0000',
                      'checksum': '3E'}
        gprmc_str = "$GPRMC,080633.000,A,4827.1601,N,03503.2484,E,,,111119,,,A*68"
        gprmc_dict = {'tag': '$GPRMC',
                      'pos_status': 'A',
                      'lat': 48.452668,
                      'lat_dir': 'N',
                      'lon': 35.05414,
                      'lon_dir': 'E',
                      'utc_timestamp': '2019-11-11T08:06:33Z',
                      'mode_ind': 'A',
                      'checksum': '68'}

        a = nmea_decoder.nmea_decode(gpgga_str, False)
        self.assertEqual(a, gpgga_dict)

        b = nmea_decoder.nmea_decode(gprmc_str, False)
        self.assertEqual(b, gprmc_dict)

    def test_empty_string_with_correct_checksum(self):
        gpgga_str = "$GPGGA,,,,,,,,,,,,,,*56"
        gpgga_dict = {'tag': '$GPGGA',
                      'utc_time_raw': '',
                      'lat': 0.0,
                      'lat_dir': '',
                      'lon': 0.0,
                      'lon_dir': '',
                      'quality': '',
                      'sattelite_num': '',
                      'hdop': '',
                      'altitude': '',
                      'altitude_units': '',
                      'geoidal_separation': '',
                      'geoidal_separation_val': '',
                      'age': '',
                      'dif_reference': '',
                      'checksum': '56'}
        a = nmea_decoder.nmea_decode(gpgga_str)
        self.assertEqual(a, gpgga_dict)

    def test_W_and_S_location(self):
        gpgga_str = "$GPGGA,080633.000,4827.1601,S,03503.2484,W,1,05,5.1,86.0,M,,,,0000*31"
        gpgga_dict = {'tag': '$GPGGA',
                      'utc_time_raw': '080633.000',
                      'lat': -48.452668,
                      'lat_dir': 'S',
                      'lon': -35.05414,
                      'lon_dir': 'W',
                      'quality': '1',
                      'sattelite_num': '05',
                      'hdop': '5.1',
                      'altitude': '86.0',
                      'altitude_units': 'M',
                      'dif_reference': '0000',
                      'checksum': '31'}
        gprmc_str = "$GPRMC,080633.000,A,4827.1601,S,03503.2484,W,,,111119,,,A*67"
        gprmc_dict = {'tag': '$GPRMC',
                      'pos_status': 'A',
                      'lat': -48.452668,
                      'lat_dir': 'S',
                      'lon': -35.05414,
                      'lon_dir': 'W',
                      'utc_timestamp': '2019-11-11T08:06:33Z',
                      'mode_ind': 'A',
                      'checksum': '67'}

        a = nmea_decoder.nmea_decode(gpgga_str, False)
        self.assertEqual(a, gpgga_dict)

        b = nmea_decoder.nmea_decode(gprmc_str, False)
        self.assertEqual(b, gprmc_dict)

    def test_empty_string_with_correct_checksum_non_empty_values(self):
        gpgga_str = "$GPGGA,,,,,,,,,,,,,,*56"
        gpgga_dict = {'tag': '$GPGGA',
                      'lat': 0.0,
                      'lon': 0.0,
                      'checksum': '56'}
        a = nmea_decoder.nmea_decode(gpgga_str, zero_values=False)
        self.assertEqual(a, gpgga_dict)


if __name__ == '__main__':
    unittest.main()
