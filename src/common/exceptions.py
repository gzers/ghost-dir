# -*- coding: utf-8 -*-
"""
Global Exception Definitions
All custom exceptions for the project
"""


class GhostDirException(Exception):
    """Base exception for Ghost-Dir"""
    pass


class ValidationError(GhostDirException):
    """Data validation error"""
    pass


class DriverError(GhostDirException):
    """Driver layer error"""
    pass


class DAOError(GhostDirException):
    """Data access layer error"""
    pass


class ServiceError(GhostDirException):
    """Service layer error"""
    pass


class ConfigError(GhostDirException):
    """Configuration error"""
    pass
