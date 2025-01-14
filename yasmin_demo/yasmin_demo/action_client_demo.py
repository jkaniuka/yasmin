#!/usr/bin/env python3

# Copyright (C) 2023  Miguel Ángel González Santamarta

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import rclpy

from simple_node import Node
from action_tutorials_interfaces.action import Fibonacci

from yasmin import CbState
from yasmin import Blackboard
from yasmin import StateMachine
from yasmin_ros import AcionState
from yasmin_ros.basic_outcomes import SUCCEED, ABORT, CANCEL
from yasmin_viewer import YasminViewerPub


class FibonacciState(AcionState):
    def __init__(self, node: Node) -> None:
        super().__init__(
            node,  # node
            Fibonacci,  # action type
            "/fibonacci",  # action name
            self.create_goal_handler,  # cb to create the goal
            None,  # outcomes. Includes (SUCCEED, ABORT, CANCEL)
            self.response_handler  # cb to process the response
        )

    def create_goal_handler(self, blackboard: Blackboard) -> Fibonacci.Goal:

        goal = Fibonacci.Goal()
        goal.order = blackboard.n
        return goal

    def response_handler(
        self,
        blackboard: Blackboard,
        response: Fibonacci.Result
    ) -> str:

        blackboard.fibo_res = response.sequence
        return SUCCEED


def set_int(blackboard: Blackboard) -> str:
    blackboard.n = 3
    return SUCCEED


def print_result(blackboard: Blackboard) -> str:
    print(f"Result: {blackboard.fibo_res}")
    return SUCCEED


class ActionClientDemoNode(Node):

    def __init__(self):
        super().__init__("yasmin_node")

        # create a state machine
        sm = StateMachine(outcomes=["outcome4"])

        # add states
        sm.add_state("SETTING_INT", CbState([SUCCEED], set_int),
                     transitions={SUCCEED: "CALLING_FIBONACCI"})
        sm.add_state("CALLING_FIBONACCI", FibonacciState(self),
                     transitions={SUCCEED: "PRINTING_RESULT",
                                  CANCEL: "outcome4",
                                  ABORT: "outcome4"})
        sm.add_state("PRINTING_RESULT", CbState([SUCCEED], print_result),
                     transitions={SUCCEED: "outcome4"})

        # pub
        YasminViewerPub(self, "YASMIN_ACTION_CLIENT_DEMO", sm)

        # execute
        outcome = sm()
        print(outcome)


# main
def main(args=None):

    print("yasmin_action_client_demo")
    rclpy.init(args=args)
    node = ActionClientDemoNode()
    node.join_spin()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
