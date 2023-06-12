from typing import List


class SwitchesExceptions(Exception):
    """Exception parent class."""

    @staticmethod
    def correction(switches_to_do, **kwargs):
        pass


class SwitchIdNotInt(SwitchesExceptions):
    """Exception class for when any of the input switch ID is not int."""
    @staticmethod
    def correction(switches_to_do: List[int], **kwargs) -> List[int]:
        """Return list with default switch IDs when input list is not all integers.
            Parameters:
                switches_to_do: Input switches
            Returns:
                List with default switches ID"""
        print('Inputs not all integers, reverting to defaults')
        return [100, 200, 300, 400, 500]


class SwitchIdOutsideRange(SwitchesExceptions):
    """Exception for when an input switch ID is outside range"""
    @staticmethod
    def correction(switches_to_do, **kwargs):
        """Return updated switch ID list
            Parameters:
                switches_to_do: Input switches
            Returns:
                List with updated switches ID"""
        print('Switches ID outside range, removing offending IDs')
        switches_to_do = [ii for ii in switches_to_do if ii >= kwargs['min']]
        switches_to_do = [ii for ii in switches_to_do if ii <= kwargs['max']]
        return switches_to_do


class NumberOfSwitches(SwitchesExceptions):
    """Exception for when input list with switch IDs has length greater than 5."""
    @staticmethod
    def correction(switches_to_do, **kwargs):
        """Return updated switch ID list
            Parameters:
                switches_to_do: Input switches
            Returns:
                Truncated list of length 5"""
        print('Only 5 switch allowed for plotting, truncating...')
        return switches_to_do[:5]
