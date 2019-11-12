import unittest
import nmea_decoder


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
        gpgga_dict = {'utc': '080633.000',
                      'lat': '4827.1601',
                      'lat_dir': 'N',
                      'lon': '03503.2484',
                      'lon_dir': 'E',
                      'quality': '1',
                      'sattelite_num': '05',
                      'hdop': '5.1',
                      'altitude': '86.0',
                      'altitude_units': 'M',
                      'geoidal_separation': '',
                      'geoidal_separation_val': '',
                      'age': '', 'dif_reference': '0000',
                      'checksum': '3E'}
        gprmc_str = "$GPRMC,080633.000,A,4827.1601,N,03503.2484,E,,,111119,,,A*68"
        gprmc_dict = {'utc': '080633.000',
                      'pos_status': 'A',
                      'lat': '4827.1601',
                      'lat_dir': 'N',
                      'lon': '03503.2484',
                      'lon_dir': 'E',
                      'speed_knots': '',
                      'true_course': '',
                      'date': '111119',
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
        gpgga_dict = {'utc': '080633.000',
                      'lat': '4827.1601',
                      'lat_dir': 'N',
                      'lon': '03503.2484',
                      'lon_dir': 'E',
                      'quality': '1',
                      'sattelite_num': '05',
                      'hdop': '5.1',
                      'altitude': '86.0',
                      'altitude_units': 'M',
                      'dif_reference': '0000',
                      'checksum': '3E'}
        gprmc_str = "$GPRMC,080633.000,A,4827.1601,N,03503.2484,E,,,111119,,,A*68"
        gprmc_dict = {'utc': '080633.000',
                      'pos_status': 'A',
                      'lat': '4827.1601',
                      'lat_dir': 'N',
                      'lon': '03503.2484',
                      'lon_dir': 'E',
                      'date': '111119',
                      'mode_ind': 'A',
                      'checksum': '68'}

        a = nmea_decoder.nmea_decode(gpgga_str, False)
        self.assertEqual(a, gpgga_dict)

        b = nmea_decoder.nmea_decode(gprmc_str, False)
        self.assertEqual(b, gprmc_dict)


if __name__ == '__main__':
    unittest.main()
