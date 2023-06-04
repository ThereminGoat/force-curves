import os
import pandas as pd


class DataProcess:

    def main(self):
        """Main program."""

        file_paths = self.rummage_through()

        return file_paths

    def rummage_through(self) -> list[str]:
        """Return a list with the file paths of all data file.

        Parameters:

        Returns:
            List with file paths of all data files
        """
        file_paths = []
        switches_directories = self.get_switches_directories()

        for ii in switches_directories:
            file_paths.extend(self.get_files_name(ii))

        return file_paths

    @staticmethod
    def get_files_name(switch_dir: str) -> list[str]:
        """Return a list with all the directories of data in the specific switch directory.

        Parameters:
            switch_dir: Name of directory for the specific switch

        Returns:
            List with file paths with data in the directory
        """
        # Find all the files in the dir and create a list with the one that hold the raw data
        # Might be more than one.
        files_in_folder = os.listdir(switch_dir)
        # All files with raw data
        switch_files_name = [ii for ii in files_in_folder if ii.endswith('Data Construction.xlsx')]
        # All file paths with raw data
        switch_files_path = [switch_dir + '/' + ii for ii in switch_files_name]

        return switch_files_path

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

