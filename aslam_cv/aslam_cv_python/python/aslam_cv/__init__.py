# Import the numpy to Eigen type conversion.
import numpy_eigen

# Try the actual import rather than checking a file path on disk: under
# colcon's --symlink-install, __file__ is a symlink back into the source
# tree, so os.path.realpath(__file__) (the old check here) resolves past
# the install directory back to source -- where the compiled .so never
# lives -- and this would always report "not compiled" even when it is.
# A relative import resolves through the package's real __path__ at
# runtime instead, so it works the same whether colcon copied or
# symlinked the install.
isCompiled = False
try:
    # Import the the C++ exports from your package library.
    from .libaslam_cv_python import *
    # Import other files in the directory
    # from mypyfile import *
    isCompiled = True
except ImportError:
    print("Warning: the package aslam_cv_python is not compiled. Type 'rosmake aslam_cv_python' if you need this.")
    PACKAGE_IS_NOT_COMPILED = True
