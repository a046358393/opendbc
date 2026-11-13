import unittest

from opendbc.car.toyota.carstate import AccelPersonality, get_accel_personality


class TestDriveMode(unittest.TestCase):
  def test_acceleration_profile_mapping(self):
    # Values must match cereal.Log.LongitudinalPersonality:
    # aggressive=0 (SPORT), standard=1 (NORMAL), relaxed=2 (ECO).
    self.assertEqual(int(get_accel_personality(0, 0)), 1)
    self.assertEqual(int(get_accel_personality(0, 1)), 2)
    self.assertEqual(int(get_accel_personality(1, 0)), 0)
    self.assertEqual(int(get_accel_personality(1, 1)), 0)


if __name__ == "__main__":
  unittest.main()
