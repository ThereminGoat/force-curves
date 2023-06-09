class SwitchesExceptions(Exception):

    @staticmethod
    def correction(switches_to_do, **kwargs):
        pass


class SwitchIdNotInt(SwitchesExceptions):

    @staticmethod
    def correction(switches_to_do, **kwargs):
        print('Inputs not all integers, reverting to defaults')
        return [100, 200, 300, 400, 500]


class SwitchIdOutsideRange(SwitchesExceptions):

    @staticmethod
    def correction(switches_to_do, **kwargs):
        print('Switches ID outside range, removing offending IDs')

        switches_to_do = [ii for ii in switches_to_do if ii >= kwargs['min']]
        switches_to_do = [ii for ii in switches_to_do if ii <= kwargs['max']]
        return switches_to_do


class NumberOfSwitches(SwitchesExceptions):

    @staticmethod
    def correction(switches_to_do, **kwargs):
        print('Only 5 switch allowed for plotting, truncating...')
        return switches_to_do[:5]
