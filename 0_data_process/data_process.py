import os
import sqlite3
import pandas as pd


class DataProcess:

    def main(self):
        """Main program."""

        # For each file with data
        for ii in self.rummage_through()[0:4]:


            _dic = self.read_excel_data_file(ii)

        return _dic

    @staticmethod
    def create_conn():
        conn = None
        try:
            conn = sqlite3.connect('force_curves')
            return conn, conn.cursor()
        except Exception as E:
            print(E)

        return

    @staticmethod
    def read_excel_data_file(file_path) -> dict:
        """Return dictionary with data.

            Parameters:

            Returns:
                Returns dictionary with keys ['Downstroke', 'Upstroke'] and values dataframe
                with columns ['Force', 'Displacement', 'Switch_Name', 'Mode']
        """

        # Get name of switch
        _df = pd.read_excel(file_path, header=None, usecols='B', skiprows=1,
                            sheet_name=['DataTable'])
        switch_name = _df['DataTable'].iloc[0, 0]

        # Get dictionary with data from Excel. Keys are Downstroke, Upstroke
        # and columns are 2 (force) and 11 (displacement).
        _dic = pd.read_excel(file_path, header=None, usecols='C,L',
                             skiprows=5, sheet_name=['Downstroke', 'Upstroke'])

        # Rename columns and add switch name and mode
        for kk, df in _dic.items():
            df.rename(columns={'2': 'Force', '11': 'Displacement'}, inplace=True)
            df['Switch_Name'] = switch_name
            df['Mode'] = kk

        return _dic

    def create_table(self):

        conn, cur = self.create_conn()

        cur.execute(""" DROP TABLE IF EXISTS force_curves """)

        _sql = """ CREATE TABLE force_curves(
                    id INTEGER PRIMARY KEY,
                    force REAL,
                    displacement REAL,
                    name CHAR(100))
                    """

        cur.execute(_sql)
        cur.close()
        conn.close()

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

