import cv_bridge
import cv2
import os
import numpy as np
import pylab as pl
import aslam_cv as acv
import sm


class BagImageDatasetReaderIterator(object):
  def __init__(self, dataset, indices=None):
    self.dataset = dataset
    if indices is None:
      self.indices = np.arange(dataset.numImages())
    else:
      self.indices = indices
    self.iter = self.indices.__iter__()

  def __iter__(self):
    return self

  def next(self):
    # required for python 2.x compatibility
    idx = next(self.iter)
    return self.dataset.getImage(idx)

  def __next__(self):
    idx = next(self.iter)
    return self.dataset.getImage(idx)


class _IndexedMessage(object):
  """One message on the target topic, as read out of an mcap/rosbag2 bag.

  `raw` is the still-serialized (CDR) message payload; it is only
  deserialized on demand (in getImage()/sortByTime() etc.) to avoid
  holding every decoded image in memory at once.
  """
  __slots__ = ("t_ns", "raw", "msg_type")

  def __init__(self, t_ns, raw, msg_type):
    self.t_ns = t_ns
    self.raw = raw
    self.msg_type = msg_type


class BagImageDatasetReader(object):
  def __init__(self, bagfile, imagetopic, bag_from_to=None, perform_synchronization=False, bag_freq=None):
    self.bagfile = bagfile
    self.topic = imagetopic
    self.perform_synchronization = perform_synchronization
    self.uncompress = None
    if imagetopic is None:
      raise RuntimeError(
          "Please pass in a topic name referring to the image stream in the bag file\n{0}".format(self.bagfile))

    self.CVB = cv_bridge.CvBridge()
    self._msg_class_cache = {}

    # ROS2 bags (mcap storage) only support sequential reading, unlike
    # ROS1's rosbag which allowed random access by (topic, position). We
    # therefore do a single sequential pass up front to build an
    # in-memory index of every message on the target topic, and support
    # "random access" (sortByTime/truncate*/getImage) against that index.
    self._messages = self._readTopicMessages(bagfile, imagetopic)
    if not self._messages:
      raise RuntimeError("Could not find topic {0} in {1}.".format(imagetopic, self.bagfile))

    self.indices = np.arange(len(self._messages))

    # sort the indices by header.stamp
    self.indices = self.sortByTime(self.indices)

    # go through the bag and remove the indices outside the timespan [bag_start_time, bag_end_time]
    if bag_from_to:
      self.indices = self.truncateIndicesFromTime(self.indices, bag_from_to)

    # go through and remove indices not at the correct frequency
    if bag_freq:
      self.indices = self.truncateIndicesFromFreq(self.indices, bag_freq)

  def _readTopicMessages(self, bagfile, imagetopic):
    import rosbag2_py
    reader = rosbag2_py.SequentialReader()
    reader.open(
        rosbag2_py.StorageOptions(uri=bagfile, storage_id="mcap"),
        rosbag2_py.ConverterOptions(input_serialization_format="cdr",
                                     output_serialization_format="cdr"),
    )
    type_by_topic = {t.name: t.type for t in reader.get_all_topics_and_types()}
    msg_type = type_by_topic.get(imagetopic)
    messages = list()
    while reader.has_next():
      topic, raw, t_ns = reader.read_next()
      if topic != imagetopic:
        continue
      messages.append(_IndexedMessage(t_ns, raw, msg_type))
    return messages

  def _msgClass(self, type_string):
    cls = self._msg_class_cache.get(type_string)
    if cls is None:
      from rosidl_runtime_py.utilities import get_message
      cls = get_message(type_string)
      self._msg_class_cache[type_string] = cls
    return cls

  def _deserialize(self, record):
    from rclpy.serialization import deserialize_message
    return deserialize_message(record.raw, self._msgClass(record.msg_type))

  @staticmethod
  def _headerStampSec(data):
    # ROS2 message fields are `sec`/`nanosec` (ROS1 used `secs`/`nsecs`).
    return data.header.stamp.sec + data.header.stamp.nanosec / 1.0e9

  # sort the ros messegaes by the header time not message time
  def sortByTime(self, indices):
    self.timestamp_corrector = sm.DoubleTimestampCorrector()
    timestamps = list()
    for idx in indices:
      record = self._messages[idx]
      data = self._deserialize(record)
      header_sec = self._headerStampSec(data)
      timestamps.append(header_sec * 1e9)
      if self.perform_synchronization:
        self.timestamp_corrector.correctTimestamp(header_sec, record.t_ns * 1.0e-9)

    sorted_tuples = sorted(zip(timestamps, indices))
    sorted_indices = [tuple_value[1] for tuple_value in sorted_tuples]
    return sorted_indices

  def truncateIndicesFromTime(self, indices, bag_from_to):
    # get the timestamps
    timestamps = list()
    for idx in indices:
      data = self._deserialize(self._messages[idx])
      timestamps.append(self._headerStampSec(data))

    bagstart = min(timestamps)
    baglength = max(timestamps) - bagstart

    # some value checking
    if bag_from_to[0] >= bag_from_to[1]:
      raise RuntimeError("Bag start time must be bigger than end time.".format(bag_from_to[0]))
    if bag_from_to[0] < 0.0:
      sm.logWarn("Bag start time of {0} s is smaller 0".format(bag_from_to[0]))
    if bag_from_to[1] > baglength:
      sm.logWarn("Bag end time of {0} s is bigger than the total length of {1} s".format(
          bag_from_to[1], baglength))

    # find the valid timestamps
    valid_indices = []
    for idx, timestamp in zip(indices, timestamps):
      if timestamp >= (bagstart + bag_from_to[0]) and timestamp <= (bagstart + bag_from_to[1]):
        valid_indices.append(idx)
    sm.logWarn(
        "BagImageDatasetReader: truncated {0} / {1} images (from-to).".format(len(indices) - len(valid_indices), len(indices)))
    return valid_indices

  def truncateIndicesFromFreq(self, indices, freq):

    # some value checking
    if freq < 0.0:
      raise RuntimeError("Frequency {0} Hz is smaller 0".format(freq))

    # find the valid timestamps
    timestamp_last = -1
    valid_indices = []
    for idx in indices:
      data = self._deserialize(self._messages[idx])
      timestamp = self._headerStampSec(data)
      if timestamp_last < 0.0:
        timestamp_last = timestamp
        valid_indices.append(idx)
        continue
      if (timestamp - timestamp_last) >= 1.0 / freq:
        timestamp_last = timestamp
        valid_indices.append(idx)
    sm.logWarn(
      "BagImageDatasetReader: truncated {0} / {1} images (frequency)".format(len(indices) - len(valid_indices), len(indices)))
    return valid_indices

  def __iter__(self):
    # Reset the bag reading
    return self.readDataset()

  def readDataset(self):
    return BagImageDatasetReaderIterator(self, self.indices)

  def readDatasetShuffle(self):
    indices = self.indices
    np.random.shuffle(indices)
    return BagImageDatasetReaderIterator(self, indices)

  def numImages(self):
    return len(self.indices)

  def getImage(self, idx):
    record = self._messages[idx]
    data = self._deserialize(record)
    if self.perform_synchronization:
      timestamp = acv.Time(self.timestamp_corrector.getLocalTime(
          self._headerStampSec(data)))
    else:
      timestamp = acv.Time(data.header.stamp.sec,
                           data.header.stamp.nanosec)
    # ROS2 message type string, e.g. "sensor_msgs/msg/CompressedImage".
    msg_type = record.msg_type
    if msg_type == 'sensor_msgs/msg/CompressedImage':
      # compressed images only have either mono or BGR normally (png and jpeg)
      # https://github.com/ros-perception/vision_opencv/blob/906d326c146bd1c6fbccc4cd1268253890ac6e1c/cv_bridge/src/cv_bridge.cpp#L480-L506
      img_data = np.array(self.CVB.compressed_imgmsg_to_cv2(data))
      if len(img_data.shape) > 2 and img_data.shape[2] == 3:
        img_data = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
    elif msg_type == 'sensor_msgs/msg/Image':
      if data.encoding == "16UC1" or data.encoding == "mono16":
        image_16u = np.array(self.CVB.imgmsg_to_cv2(data))
        img_data = (image_16u / 256).astype("uint8")
      elif data.encoding == "8UC1" or data.encoding == "mono8":
        img_data = np.array(self.CVB.imgmsg_to_cv2(data))
      elif data.encoding == "8UC3" or data.encoding == "bgr8":
        img_data = np.array(self.CVB.imgmsg_to_cv2(data))
        img_data = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
      elif data.encoding == "rgb8":
        img_data = np.array(self.CVB.imgmsg_to_cv2(data))
        img_data = cv2.cvtColor(img_data, cv2.COLOR_RGB2GRAY)
      elif data.encoding == "8UC4" or data.encoding == "bgra8":
        img_data = np.array(self.CVB.imgmsg_to_cv2(data))
        img_data = cv2.cvtColor(img_data, cv2.COLOR_BGRA2GRAY)
      # bayes encodings conversions from
      # https://github.com/ros-perception/image_pipeline/blob/6caf51bd4484ae846cd8a199f7a6a4b060c6373a/image_proc/src/libimage_proc/processor.cpp#L70
      elif data.encoding == "bayer_rggb8":
        img_data = np.array(self.CVB.imgmsg_to_cv2(data))
        img_data = cv2.cvtColor(img_data, cv2.COLOR_BAYER_BG2GRAY)
      elif data.encoding == "bayer_bggr8":
        img_data = np.array(self.CVB.imgmsg_to_cv2(data))
        img_data = cv2.cvtColor(img_data, cv2.COLOR_BAYER_RG2GRAY)
      elif data.encoding == "bayer_gbrg8":
        img_data = np.array(self.CVB.imgmsg_to_cv2(data))
        img_data = cv2.cvtColor(img_data, cv2.COLOR_BAYER_GR2GRAY)
      elif data.encoding == "bayer_grbg8":
        img_data = np.array(self.CVB.imgmsg_to_cv2(data))
        img_data = cv2.cvtColor(img_data, cv2.COLOR_BAYER_GB2GRAY)
      else:
        raise RuntimeError(
            "Unsupported Image Encoding: '{}'\nSupported are: "
            "16UC1 / mono16, 8UC1 / mono8, 8UC3 / rgb8 / bgr8, 8UC4 / bgra8, "
            "bayer_rggb8, bayer_bggr8, bayer_gbrg8, bayer_grbg8".format(data.encoding))
    else:
      # NOTE: the legacy Skybotix 'mv_cameras/ImageSnappyMsg' type from the
      # original ROS1 kalibr is not supported here (ROS2/rosbag2 bags
      # would never carry it in practice).
      raise RuntimeError(
        "Unsupported Image Type: '{}'\nSupported are: "
        "sensor_msgs/msg/CompressedImage, sensor_msgs/msg/Image".format(msg_type))
    return (timestamp, img_data)
