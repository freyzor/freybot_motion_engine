import unittest
import mock
from romobilize.poses import PosePlayer, NoPosesError, PLAY_FRAME_ZERO, PlayFrame

FRAME_TIME = 0.5
POSE_1 = mock.sentinel.POSE_1


class PosePlayerTestCase(unittest.TestCase):
    def test_init_poses_are_null_raises(self):
        with self.assertRaises(NoPosesError):
            PosePlayer(None)

    def test_init_no_poses_raises(self):
        with self.assertRaises(NoPosesError):
            PosePlayer(None)

    def test_init_single_poses_sets_play_time_zero(self):
        player = PosePlayer([POSE_1], FRAME_TIME)
        self.assertEquals(0, player.play_time_sec)

    def test_init_two_poses_sets_play_time_is_frame_time(self):
        player = PosePlayer([POSE_1]*2, FRAME_TIME)
        self.assertEquals(FRAME_TIME, player.play_time_sec)

    def test_init_three_poses_sets_play_time_is_two_fame_times(self):
        player = PosePlayer([POSE_1]*3, FRAME_TIME)
        self.assertEquals(FRAME_TIME*2, player.play_time_sec)

    def test_get_play_frame_at_zero_with_a_pose_gives_zero_frame(self):
        player = PosePlayer([POSE_1], FRAME_TIME)
        frame = player.get_play_frame(0.0)
        self.assertEquals(frame, PLAY_FRAME_ZERO)

    def test_get_play_frame_at_zero_with_poses_gives_zero_frame(self):
        player = PosePlayer([POSE_1]*11, FRAME_TIME)
        frame = player.get_play_frame(0.0)
        self.assertEquals(frame, PLAY_FRAME_ZERO)

    def test_get_play_frame_at_play_time_with_poses_gives_end_frame(self):
        num_frames = 11
        player = PosePlayer([POSE_1]*num_frames, FRAME_TIME)
        frame = player.get_play_frame(player.play_time_sec)
        self.assertEquals(frame, PlayFrame(num_frames-1, 0))

    def test_get_play_frame_at_half_point_return_frame_and_offset(self):
        num_frames = 11
        time_sec = FRAME_TIME * num_frames / 2.0
        player = PosePlayer([POSE_1]*num_frames, FRAME_TIME)
        frame = player.get_play_frame(time_sec)
        self.assertEquals(frame, PlayFrame(5, 0.5))

    def test_get_play_frame_at_quarter_point_return_frame_and_offset(self):
        num_frames = 11
        time_sec = FRAME_TIME * num_frames / 4.0
        player = PosePlayer([POSE_1]*num_frames, FRAME_TIME)
        frame = player.get_play_frame(time_sec)
        self.assertEquals(frame, PlayFrame(2, 0.75))

if __name__ == '__main__':
    unittest.main()
