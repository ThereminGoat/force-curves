import os
import pandas as pd


class DataProcess:

    def main(self):


        self.rummage_through()

    def rummage_through(self):

        switches_directories = self.get_switches_directories()

        for ii in switches_directories:
            self.get_file_name(ii)

    @staticmethod
    def get_file_name(ii):

        files_in_folder = os.listdir(ii)
        iii = [ii for ii in files_in_folder if ii.endswith('Raw Data CSV.csv')]

        print(iii)

        #pd.read_csv(file_name)

    @staticmethod
    def get_switches_directories() -> list[str]:
        """Return a list with the directories of all switches.

            :param:
                None
            :return:
                List with the directories of all switches
            """
        directory_names = [ii[0] for ii in os.walk('../')]
        # Remove hidden directories and current directory
        directory_names = [ii for ii in directory_names if (
                not ii.startswith('../.') and not ii.startswith('../0_data'))]

        return directory_names[1:]

