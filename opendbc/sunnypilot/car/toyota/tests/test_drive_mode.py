import unittest

from opendbc.car import structs
from opendbc.car.toyota.values import ToyotaFlags
from opendbc.car.toyota.carstate import AccelPersonality, get_accel_personality, is_toyota_drive_mode_enabled


class TestDriveMode(unittest.TestCase):
  def test_acceleration_profile_mapping(self):
    # Values must match cereal.Log.LongitudinalPersonality:
    # aggressive=0 (SPORT), standard=1 (NORMAL), relaxed=2 (ECO).
    self.assertEqual(int(get_accel_personality(0, 0)), 1)
    self.assertEqual(int(get_accel_personality(0, 1)), 2)
    self.assertEqual(int(get_accel_personality(1, 0)), 0)
    self.assertEqual(int(get_accel_personality(1, 1)), 0)


  def test_drive_mode_requires_tss2_longitudinal_and_user_preference(self):
    cp = structs.CarParams(flags=ToyotaFlags.TSS2.value)
    cp.openpilotLongitudinalControl = True
    self.assertTrue(is_toyota_drive_mode_enabled(cp, True))
    self.assertFalse(is_toyota_drive_mode_enabled(cp, False))

  def test_drive_mode_is_disabled_without_openpilot_longitudinal(self):
    cp = structs.CarParams(flags=ToyotaFlags.TSS2.value)
    cp.openpilotLongitudinalControl = False
    self.assertFalse(is_toyota_drive_mode_enabled(cp, True))

  def test_drive_mode_is_disabled_outside_tss2(self):
    cp = structs.CarParams(flags=0)
    cp.openpilotLongitudinalControl = True
    self.assertFalse(is_toyota_drive_mode_enabled(cp, True))

  def test_drive_mode_is_disabled_for_secoc(self):
    cp = structs.CarParams(flags=ToyotaFlags.TSS2.value | ToyotaFlags.SECOC.value)
    cp.openpilotLongitudinalControl = True
    self.assertFalse(is_toyota_drive_mode_enabled(cp, True))


if __name__ == "__main__":
  unittest.main()
