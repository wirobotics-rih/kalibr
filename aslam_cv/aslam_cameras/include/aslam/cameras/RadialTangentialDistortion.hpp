#ifndef ASLAM_CAMERAS_RT_DISTORTION_HPP
#define ASLAM_CAMERAS_RT_DISTORTION_HPP

#include <Eigen/Dense>
#include <boost/serialization/nvp.hpp>
#include "StaticAssert.hpp"
#include <boost/serialization/split_member.hpp>
#include <boost/serialization/version.hpp>
#include <sm/boost/serialization.hpp>

namespace sm {
class PropertyTree;
}  // namespace sm

namespace aslam {
namespace cameras {

/**
 * \class RadialTangentialDistortion
 * \brief The Brown-Conrady distortion model for pinhole cameras, with THREE
 *        radial terms and two tangential ones.
 *
 * Upstream aslam_cv truncates the radial series after k2:
 *
 *     rad = k1 r^2 + k2 r^4
 *
 * which is the classic plumb-bob of photogrammetry, and upstream's answer for a
 * lens that needs more is EquidistantDistortion. OpenCV's `plumb_bob` carries a
 * third term, and every intrinsic this workspace solves is fitted by OpenCV, so
 * without k3 our K cannot be handed to this model at all -- it has to be
 * undistorted away first, which puts an iterative inverse between the corners
 * and the optimiser. This adds the term instead:
 *
 *     rad = k1 r^2 + k2 r^4 + k3 r^6
 *
 * Measured on p005 (ALLEX unit) before doing so, refitting each camera with k3
 * pinned at zero rather than deleting it from a five-term fit:
 *
 *     camera      terms   reproj rms   undistortion split-half   board dome
 *     wide          5       0.9115          14.0 px               1.38 mm
 *     wide          4       1.8007          20.1 px               2.09 mm
 *     realsense     5       0.9362          23.4 px               0.92 mm
 *     realsense     4       1.0286          24.2 px               0.88 mm
 *
 * The board's bow is measured independently (1.36 mm, by two vendor-calibrated
 * cameras that fit no distortion model), so the wide's 2.09 is not a tie-break
 * -- a four-term fit of that lens is wrong about the target by 0.7 mm and
 * reprojects twice as badly. The RealSense would survive on four; the wide
 * would not.
 *
 * PARAMETER ORDER IS OPENCV'S: k1, k2, p1, p2, k3. k3 is appended rather than
 * placed after k2 so that a coefficient vector from cv2.calibrateCamera goes
 * into setParameters unchanged, and so that the first four keep the meaning
 * every existing caller gives them.
 *
 * \todo outline the math here and provide a reference. What is the original reference?
 *
 *
 * The usual model of a pinhole camera follows these steps:
 *   - Transformation: Transform the point into a coordinate frame associated with the camera
 *   - Normalization:  Project the point onto the normalized image plane: \f$\mathbf y := \left[ x/z,y/z\right] \f$
 *   - Distortion:     apply a nonlinear transformation to \f$y\f$ to account for radial and tangential distortion of the lens
 *   - Projection:     Project the point into the image using a standard \f$3 \time 3\f$ projection matrix
 *
 * This class represents a standard implementation of the distortion block. The function "distort" applies this nonlinear transformation.
 * The function "undistort" applies the inverse transformation. Note that the inverse transformation in this case is not avaialable in 
 * closed form and so it is computed iteratively.
 * 
 */
class RadialTangentialDistortion {
 public:

  enum {
    IntrinsicsDimension = 5
  };
  enum {
    DesignVariableDimension = IntrinsicsDimension
  };

  /// \brief The default constructor sets all values to zero. 
  RadialTangentialDistortion();

  /// \brief A constructor that initializes all values. k3 defaults to zero,
  ///        which is exactly upstream's model, so existing callers are unchanged.
  RadialTangentialDistortion(double k1, double k2, double p1, double p2);

  /// \brief A constructor that initializes all values, OpenCV's order.
  RadialTangentialDistortion(double k1, double k2, double p1, double p2,
                             double k3);

  RadialTangentialDistortion(const sm::PropertyTree & config);

  virtual ~RadialTangentialDistortion();

  /** 
   * \brief Apply distortion to a point in the normalized image plane
   * 
   * @param y The point in the normalized image plane. After the function, this point is distorted.
   */
  template<typename DERIVED_Y>
  void distort(const Eigen::MatrixBase<DERIVED_Y> & y) const;

  /** 
   * 
   * \brief Apply distortion to a point in the normalized image plane
   * 
   * @param y The point in the normalized image plane. After the function, this point is distorted.
   * @param outJy The Jacobian of the distortion function with respect to small changes in the input point.
   */
  template<typename DERIVED_Y, typename DERIVED_JY>
  void distort(const Eigen::MatrixBase<DERIVED_Y> & y,
               const Eigen::MatrixBase<DERIVED_JY> & outJy) const;

  /** 
   * \brief Apply undistortion to recover a point in the normalized image plane.
   * 
   * @param y The distorted point. After the function, this point is in the normalized image plane.
   */
  template<typename DERIVED>
  void undistort(const Eigen::MatrixBase<DERIVED> & y) const;

  /** 
   * \brief Apply undistortion to recover a point in the normalized image plane.
   * 
   * @param y The distorted point. After the function, this point is in the normalized image plane.
   * @param outJy The Jacobian of the undistortion function with respect to small changes in the input point.
   */
  template<typename DERIVED, typename DERIVED_JY>
  void undistort(const Eigen::MatrixBase<DERIVED> & y,
                 const Eigen::MatrixBase<DERIVED_JY> & outJy) const;

  /** 
   * \brief Apply distortion to the point and provide the Jacobian of the distortion with respect to small changes in the distortion parameters
   * 
   * @param imageY the point in the normalized image plane.
   * @param outJd  the Jacobian of the distortion with respect to small changes in the distortion parameters.
   */
  template<typename DERIVED_Y, typename DERIVED_JD>
  void distortParameterJacobian(
      const Eigen::MatrixBase<DERIVED_Y> & imageY,
      const Eigen::MatrixBase<DERIVED_JD> & outJd) const;

  /** 
   * \brief A function for compatibility with the aslam backend. This implements an update of the distortion parameter.
   * 
   * @param v A double array representing the update vector.
   */
  void update(const double * v);

  /** 
   * \brief A function for compatibility with the aslam backend. 
   * 
   * @param v The number of parameters expected by the update equation. This should also define the number of columns in the matrix returned by distortParameterJacobian.
   */
  int minimalDimensions() const;

  /** 
   * \brief A function for compatibility with the aslam backend. 
   * 
   * @param P This matrix is resized and filled with parameters representing the full state of the distortion. 
   */
  void getParameters(Eigen::MatrixXd & P) const;

  /** 
   * \brief A function for compatibility with the aslam backend. 
   * 
   * @param P The full state of the distortion class is set from the matrix of parameters.
   */
  void setParameters(const Eigen::MatrixXd & P);

  Eigen::Vector2i parameterSize() const;

  /// \brief the first radial distortion parameter
  double k1() {
    return _k1;
  }
  /// \brief the second radial distortion parameter
  double k2() {
    return _k2;
  }
  /// \brief the first tangential distortion parameter
  double p1() {
    return _p1;
  }
  /// \brief the second tangential distortion parameter
  double p2() {
    return _p2;
  }
  /// \brief the third radial distortion parameter
  double k3() {
    return _k3;
  }

  void clear() {
    _k1 = 0.0;
    _k2 = 0.0;
    _p1 = 0.0;
    _p2 = 0.0;
    _k3 = 0.0;
  }

  /// \brief Compatibility with boost::serialization.
  /// Bumped to 1 when k3 was added. `load` reads a version-0 archive and
  /// leaves k3 at zero, which is what that archive meant.
  enum {
    CLASS_SERIALIZATION_VERSION = 1
  };BOOST_SERIALIZATION_SPLIT_MEMBER();
  template<class Archive>
  void load(Archive & ar, const unsigned int version);
  template<class Archive>
  void save(Archive & ar, const unsigned int version) const;

  bool isBinaryEqual(const RadialTangentialDistortion & rhs) const;

  static RadialTangentialDistortion getTestDistortion();

  /// \brief the first radial distortion parameter
  double _k1;
  /// \brief the second radial distortion parameter
  double _k2;
  /// \brief the first tangential distortion parameter
  double _p1;
  /// \brief the second tangential distortion parameter
  double _p2;
  /// \brief the third radial distortion parameter. Last, to keep OpenCV's
  ///        coefficient order (k1, k2, p1, p2, k3).
  double _k3;

};

}  // namespace cameras
}  // namespace aslam

#include "implementation/RadialTangentialDistortion.hpp"

SM_BOOST_CLASS_VERSION (aslam::cameras::RadialTangentialDistortion);

#endif /* ASLAM_CAMERAS_DISTORTION_HPP */
