#!/bin/bash

pkg=yasmin
ros_pkg_path=$(python3 -c "from ament_index_python.packages import get_package_share_directory; print(get_package_share_directory('$pkg'))")
py_pkg_path=$(python3 -c "import os, $pkg; print(os.path.dirname($pkg.__file__))")
pytest --cov=$py_pkg_path $ros_pkg_path/pytests/*.py