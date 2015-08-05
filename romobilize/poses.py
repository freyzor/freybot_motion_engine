from collections import namedtuple


Pose = namedtuple("Pose", field_names=["position", "rotation", "joints", ])
Joint = namedtuple("Joint", field_names=["joint_id", "angle"])
PoseSequence = namedtuple("PoseSequence", field_names=["poses"])
PlayFrame = namedtuple("PlayFrame", field_names=["index", "offset"])


PLAY_FRAME_ZERO = PlayFrame(0, 0)


class PlayerAtEnd(Exception):
    pass


class NoPosesError(Exception):
    pass


class PosePlayer(object):
    """
    Manages the playback of a pose clip.
    """
    def __init__(self, pose_sequence, frame_time=0.100):
        self.pose_sequence = pose_sequence
        self.frame_time_sec = frame_time
        if not pose_sequence:
            raise NoPosesError()
        num_poses = len(self.pose_sequence)
        self.interval_count = (num_poses - 1)
        if num_poses == 1:
            # still frame
            self.play_time_sec = 0.0
        else:
            self.play_time_sec = self.interval_count * self.frame_time_sec
        self.play_position_sec = 0.0

    def get_play_frame(self, time_sec):
        if self.play_time_sec == 0:
            return PLAY_FRAME_ZERO
        if self.play_time_sec <= time_sec:
            return PlayFrame(self.interval_count, 0.0)
        time_offset = time_sec % self.play_time_sec
        raw_index = (time_offset / self.play_time_sec) * self.interval_count
        index = int(raw_index)
        offset = raw_index - index
        return PlayFrame(index, offset)

    def get_pose_at(self, time_sec):
        if time_sec > self.play_time_sec:
            raise PlayerAtEnd()

        frame = self.get_play_frame(time_sec)
        if frame.offset < 0:
            return interpolate_poses(
                self.pose_sequence[frame.index],
                self.pose_sequence[frame.index+1],
                frame.offset
            )

        return self.pose_sequence[frame.index]

    def advance_time(self, delta_time_sec):
        new_time = self.play_position_sec + delta_time_sec
        if 0 > new_time > self.play_time_sec:
            raise PlayerAtEnd()

    def get_current_pose(self):
        return self.get_pose_at(self.play_position_sec)

    def get_pose_after(self, time_sec):
        return self.get_pose_at(self.play_position_sec + time_sec)


def interpolate_joints(joints_a, joints_b, alpha):
    joints_out = {}
    inv_alpha = 1 - alpha
    for joint_id, angle in joints_a.iteritems():
        joints_out[joint_id] = angle * inv_alpha + joints_b[joint_id] * alpha
    return joints_out


def interpolate_poses(pose_a, pose_b, alpha):
    joints = interpolate_joints(pose_a, pose_b, alpha)
    return Pose(pose_a.position, pose_a.rotation, joints)
