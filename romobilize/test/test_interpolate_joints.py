import unittest
from romobilize import poses

JOINTS_ABC_NERO = {
    "a": 0,
    "b": 0,
    "c": 0,
}

JOINTS_ABC_FIVE = {
    "a": 5,
    "b": 5,
    "c": 5,
}

JOINTS_ABC_TEN = {
    "a": 10,
    "b": 10,
    "c": 10,
}

JOINTS_ABCD_TEN = {
    "a": 10,
    "b": 10,
    "c": 10,
    "d": 10,
}

ALPHA_ZERO = 0
ALPHA_0FIVE = 0.5
ALPHA_ONE = 1


class JointTestCase(unittest.TestCase):
    def test_interpolate_joints_returns_same_joints_keys_as_orginal(self):
        joints = poses.interpolate_joints(JOINTS_ABC_NERO, JOINTS_ABCD_TEN, ALPHA_ZERO)
        self.assertSequenceEqual(set(JOINTS_ABC_NERO.keys()), set(joints.keys()))

    def test_interpolate_joints_alpha_zero_returns_first_pose(self):
        joints = poses.interpolate_joints(JOINTS_ABC_NERO, JOINTS_ABCD_TEN, ALPHA_ZERO)
        self.assertDictEqual(JOINTS_ABC_NERO, joints)

    def test_interpolate_joints_alpha_one_returns_angles_from_second_set(self):
        joints = poses.interpolate_joints(JOINTS_ABC_NERO, JOINTS_ABCD_TEN, ALPHA_ONE)
        self.assertDictEqual(JOINTS_ABC_TEN, joints)

    def test_interpolate_joints_alpha_half_returns_half_angles(self):
        joints = poses.interpolate_joints(JOINTS_ABC_NERO, JOINTS_ABCD_TEN, ALPHA_0FIVE)
        self.assertDictEqual(JOINTS_ABC_FIVE, joints)

if __name__ == '__main__':
    unittest.main()
