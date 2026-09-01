# Import the numpy to Eigen type conversion and the aslam_backend Python
# bindings first so the boost::python types referenced by
# libincremental_calibration_python's exported classes already exist.
import numpy_eigen  # noqa: F401
import aslam_backend  # noqa: F401

# Import the C++ exports from this package's compiled extension module.
from .libincremental_calibration_python import *  # noqa: F401,F403

isCompiled = True
