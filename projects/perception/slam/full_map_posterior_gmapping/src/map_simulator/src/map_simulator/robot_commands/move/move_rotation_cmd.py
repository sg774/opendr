# Copyright 2020-2022 OpenDR European Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np

from move_cmd import MoveCommand

from map_simulator.geometry.primitives import Pose


class MoveRotationCommand(MoveCommand):
    """
    Class for a command for rotating from a given start orientation, to a given target orientation,
    while remaining in the same position, in a given number of steps, by linearly interpolating the angle
    between start and end.
    """

    def __init__(self, config, callback, last_pose):
        """
        Instantiate a Rotation move command object.

        :param config: (dict) Configuration dictionary, with parameters:
                                  * "start_orientation": (float|list|np.ndarray) (Optional)[Default: last_pose.orient.)
                                                                           Starting orientation theta of the robot.
                                  * "end_orientation": (float|list|np.ndarray) Ending orientation theta of the robot.
                                  * "steps": (int) Number of desired steps/poses for the movement
                                  * "dir": (string) Direction of turning. Can be:
                                      - "cw" : for clockwise rotation.
                                      - "ccw": for counter-clockwise rotation.
                                  * "deterministic": (bool) (Optional)[Default: None] Overrides general deterministic
                                                     configuration for this move. If None, then general config applies.
                                  * "scans": (int) (Optional)[Default: None] Overrides general number of scans per move
                                             configuration for this move. If None, then general config applies.
        :param callback: (callable) Function, lambda or other callable object to be executed
                                    when calling the command object.
        :param last_pose: (Pose) Last pose of the robot before this command. Used for staying in place while rotating.
        """

        super(MoveRotationCommand, self).__init__(config, callback, last_pose)

        self._start_orientation = None
        self._end_orientation = None
        self._steps = None
        self._cw = None
        self._remove_first_pose = None

        if 'start_orientation' in config:
            start_ori = config['start_orientation']
            remove_first_pose = False
        else:
            start_ori = self._last_pose.orientation
            remove_first_pose = True

        cw = True
        if 'dir' in config:
            if config['dir'].lower() == 'ccw':
                cw = False

        self.set_start_orientation(start_ori, compute_poses=False)
        self.set_remove_first_pose(remove_first_pose, compute_poses=False)
        self.set_cw(cw, compute_poses=False)
        self.set_end_orientation(config['end_orientation'], compute_poses=False)
        self.set_steps(config['steps'], compute_poses=True)

    def set_start_orientation(self, orientation, compute_poses=True):
        """
        Sets the starting orientation of the robot.

        :param orientation: (float|list|np.ndarray) Starting orientation of the robot.
        :param compute_poses: (bool)[Default: True] Recompute the robot pose list if True.

        :return: (None)
        """

        self._start_orientation = orientation

        if compute_poses:
            self.compute_poses()

    def set_end_orientation(self, orientation, compute_poses=True):
        """
        Sets the target orientation of the robot.

        :param orientation: (float|list|np.ndarray) Starting orientation of the robot.
        :param compute_poses: (bool)[Default: True] Recompute the robot pose list if True.

        :return: (None)
        """

        self._end_orientation = orientation

        if compute_poses:
            self.compute_poses()

    def set_cw(self, cw, compute_poses=True):
        """
        Sets the direction of the rotation.

        :param cw: (bool) True if rotation is clockwise. False if counter-clockwise.
        :param compute_poses: (bool)[Default: True] Recompute the robot pose list if True.

        :return: (None)
        """

        self._cw = cw

        if compute_poses:
            self.compute_poses()

    def set_remove_first_pose(self, remove_first_pose, compute_poses=True):
        """
        Sets the remove_first_pose property, used to determine whether we want to move the robot to the starting pose
        or not. By default, if neither the starting position nor the starting orientation were explicitly defined, we
        assume that the user wants to continue with the last trajectory without jumping to a new pose.

        :param remove_first_pose: (bool) True if we want to ignore the starting pose.
                                         False if we want the robot to jump to the starting pose from wherever he was.
        :param compute_poses: (bool)[Default: True] Recompute the robot pose list if True.

        :return: (None)
        """

        self._remove_first_pose = remove_first_pose

        if compute_poses:
            self.compute_poses()

    def set_steps(self, steps, compute_poses=True):
        """
        Sets the number of poses to be interpolated.

        :param steps: (int) Number of desired poses/steps for the movement.
        :param compute_poses: (bool)[Default: True] Recompute the robot pose list if True.

        :return: (None)
        """

        self._steps = steps

        if compute_poses:
            self.compute_poses()

    def compute_poses(self):
        """
        Generates the movement's pose list and stores it internally.

        :return: (None)
        """

        if self._cw is None or \
                self._start_orientation is None or \
                self._end_orientation is None or \
                self._steps is None:
            self._poses = []
            return

        end_ori = self._end_orientation
        if self._cw:
            while self._start_orientation < end_ori:
                end_ori -= 2 * np.pi
        else:
            while self._start_orientation > end_ori:
                end_ori += 2 * np.pi

        steps = self._steps
        if self._remove_first_pose:
            steps += 1

        tmp_orientations = np.linspace(self._start_orientation, end_ori, num=steps)

        tmp_poses = [Pose(self._last_pose.position,  orientation) for orientation in tmp_orientations]

        if self._remove_first_pose:
            tmp_poses = tmp_poses[1:]

        self._poses = tmp_poses
