#include <aslam/cameras/RadialTangentialDistortion.hpp>
#include <sm/PropertyTree.hpp>
#include <sm/serialization_macros.hpp>

namespace aslam {
namespace cameras {

RadialTangentialDistortion::RadialTangentialDistortion()
    : _k1(0),
      _k2(0),
      _p1(0),
      _p2(0),
      _k3(0) {

}

RadialTangentialDistortion::RadialTangentialDistortion(double k1, double k2,
                                                       double p1, double p2)
    : _k1(k1),
      _k2(k2),
      _p1(p1),
      _p2(p2),
      _k3(0) {

}

RadialTangentialDistortion::RadialTangentialDistortion(double k1, double k2,
                                                       double p1, double p2,
                                                       double k3)
    : _k1(k1),
      _k2(k2),
      _p1(p1),
      _p2(p2),
      _k3(k3) {

}

RadialTangentialDistortion::RadialTangentialDistortion(
    const sm::PropertyTree & config) {
  _k1 = config.getDouble("k1");
  _k2 = config.getDouble("k2");
  _p1 = config.getDouble("p1");
  _p2 = config.getDouble("p2");
  // Optional, so a config written for upstream still loads and means k3 = 0.
  _k3 = config.getDouble("k3", 0.0);
}

RadialTangentialDistortion::~RadialTangentialDistortion() {

}

// aslam::backend compatibility
void RadialTangentialDistortion::update(const double * v) {
  _k1 += v[0];
  _k2 += v[1];
  _p1 += v[2];
  _p2 += v[3];
  _k3 += v[4];
}

int RadialTangentialDistortion::minimalDimensions() const {
  return IntrinsicsDimension;
}

void RadialTangentialDistortion::getParameters(Eigen::MatrixXd & S) const {
  S.resize(5, 1);
  S(0, 0) = _k1;
  S(1, 0) = _k2;
  S(2, 0) = _p1;
  S(3, 0) = _p2;
  S(4, 0) = _k3;
}

/// Takes four rows as well, meaning k3 = 0 -- that is the shape every caller
/// written against upstream passes, and silently reading past the end of it
/// would be worse than accepting it.
void RadialTangentialDistortion::setParameters(const Eigen::MatrixXd & S) {
  _k1 = S(0, 0);
  _k2 = S(1, 0);
  _p1 = S(2, 0);
  _p2 = S(3, 0);
  _k3 = (S.rows() >= 5) ? S(4, 0) : 0.0;
}

bool RadialTangentialDistortion::isBinaryEqual(
    const RadialTangentialDistortion & rhs) const {
  return SM_CHECKMEMBERSSAME(rhs, _k1) && SM_CHECKMEMBERSSAME(rhs, _k2)
      && SM_CHECKMEMBERSSAME(rhs, _p1) && SM_CHECKMEMBERSSAME(rhs, _p2)
      && SM_CHECKMEMBERSSAME(rhs, _k3);
}

Eigen::Vector2i RadialTangentialDistortion::parameterSize() const {
  return Eigen::Vector2i(5, 1);
}

RadialTangentialDistortion RadialTangentialDistortion::getTestDistortion() {
  return RadialTangentialDistortion(-0.2, 0.13, 0.0005, 0.0005, -0.01);
}

}  // namespace cameras
}  // namespace aslam
