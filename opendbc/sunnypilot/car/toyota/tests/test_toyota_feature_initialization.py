import unittest

from opendbc.car import structs
from opendbc.car.toyota.values import CAR, ToyotaFlags
from opendbc.sunnypilot.car.interfaces import _initialize_toyota
from opendbc.sunnypilot.car.toyota.values import ToyotaFlagsSP


def build_params(fingerprint=CAR.TOYOTA_COROLLA_TSS2, *, hybrid=True, longitudinal=True):
  flags = ToyotaFlags.TSS2.value
  if hybrid:
    flags |= ToyotaFlags.HYBRID.value
  CP = structs.CarParams(brand="toyota", carFingerprint=str(fingerprint), flags=flags)
  CP.openpilotLongitudinalControl = longitudinal
  return CP, structs.CarParamsSP()


class TestToyotaFeatureInitialization(unittest.TestCase):
  def test_brake_onset_is_enabled_only_for_corolla_tss2_hybrid_with_longitudinal(self):
    CP, CP_SP = build_params()
    _initialize_toyota(CP, CP_SP, {"ToyotaBrakeOnset": "1"})
    self.assertTrue(CP_SP.flags & ToyotaFlagsSP.SP_BRAKE_ONSET)

  def test_brake_onset_is_not_enabled_for_non_hybrid_corolla(self):
    CP, CP_SP = build_params(hybrid=False)
    _initialize_toyota(CP, CP_SP, {"ToyotaBrakeOnset": "1"})
    self.assertFalse(CP_SP.flags & ToyotaFlagsSP.SP_BRAKE_ONSET)

  def test_brake_onset_is_not_enabled_without_openpilot_longitudinal(self):
    CP, CP_SP = build_params(longitudinal=False)
    _initialize_toyota(CP, CP_SP, {"ToyotaBrakeOnset": "1"})
    self.assertFalse(CP_SP.flags & ToyotaFlagsSP.SP_BRAKE_ONSET)

  def test_existing_tss2_smooth_flag_is_preserved(self):
    CP, CP_SP = build_params()
    _initialize_toyota(CP, CP_SP, {
      "ToyotaTSS2Smooth": "1",
      "ToyotaBrakeOnset": "1",
    })
    self.assertTrue(CP_SP.flags & ToyotaFlagsSP.TSS2_SMOOTH)
    self.assertTrue(CP_SP.flags & ToyotaFlagsSP.SP_BRAKE_ONSET)


if __name__ == "__main__":
  unittest.main()
