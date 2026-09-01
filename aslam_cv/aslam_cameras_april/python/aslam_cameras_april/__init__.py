# Import the numpy to Eigen type conversion.
import numpy_eigen
import aslam_cv

# Try the actual import rather than checking a file path on disk -- see the
# comment in aslam_cv/__init__.py for why the old realpath+isfile check
# always reported "not compiled" under colcon's --symlink-install.
isCompiled = False
try:
    # Import the the C++ exports from your package library.
    from .libaslam_cameras_april_python import *
    # Import other files in the directory
    # from mypyfile import *
    isCompiled = True
except ImportError:
    print("Warning: the package aslam_cameras_april_python is not compiled.")
    PACKAGE_IS_NOT_COMPILED = True
