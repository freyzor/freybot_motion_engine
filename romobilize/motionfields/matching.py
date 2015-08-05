from scipy import spatial


class KDTreeMatcher(object):
    def __init__(self, pose_sequence):
        self.pose_sequence = None
        self.match_tree = self.build_index(pose_sequence)

    def build_index(self, pose_sequence):
        tree_data = []
        for pose in pose_sequence:
            tree_data.append(pose.position)
        return spatial.KDTree()
