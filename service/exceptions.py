class ServiceArgumentException(ValueError):
    pass

class ThresholdOutOfRangeException(ServiceArgumentException):
    pass

class ThresholdNotAnIntegerException(ServiceArgumentException):
    pass

class ClusterNotFoundException(ServiceArgumentException):
    pass
