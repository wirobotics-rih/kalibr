# Import the numpy to Eigen type conversion.
import numpy_eigen
from .ConfigReader import *
from .ImageDatasetReader import *
from .TargetExtractor import *

# ImuDatasetReader.py hasn't been ported off ROS1's `rosbag` yet (only
# ImageDatasetReader.py was, for kalibr_calibrate_cameras) -- it's for
# camera-IMU calibration, which is out of scope for now. Guarded so that
# camera-only tools (kalibr_calibrate_cameras) still work on a machine
# without ROS1's rosbag installed; port it the same way as
# ImageDatasetReader.py (rosbag2_py, storage_id="mcap") if/when
# kalibr_calibrate_imu_camera is needed.
try:
    from .ImuDatasetReader import *
except ImportError as e:
    import sys
    print(f"[kalibr_common] ImuDatasetReader unavailable ({e}) -- "
          f"camera-IMU calibration tools won't work until it's ported "
          f"off ROS1 rosbag; camera-only tools are unaffected.", file=sys.stderr)
