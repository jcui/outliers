class ServiceException(Exception):
    pass

class ServiceArgumentException(ServiceException):
    pass

class ServiceFailedException(ServiceException):
    pass

class ThresholdOutOfRangeException(ServiceArgumentException):
    pass

class ThresholdNotAnIntegerException(ServiceArgumentException):
    pass

class ClusterNotFoundException(ServiceArgumentException):
    pass

class CachesRequestFailedException(ServiceFailedException):
    pass
