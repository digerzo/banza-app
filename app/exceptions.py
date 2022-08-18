"""Exceptions de dominio"""

class DomainException(Exception):
    """Domain Exception base"""


class SaldoInsuficiente(DomainException):
    """El saldo es insuficiente para realizar la operacion deseada"""
