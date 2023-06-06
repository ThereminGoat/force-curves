import os
import sqlite3
import pandas as pd


class DataProcess:

    def main(self):
        """Reads data and creates SQL db with all switch downstroke/upstroke profiles."""

        # Create the SQL table
        self.create_table()
        # Get connection and cursor
        conn, cur = self.create_conn()

        # For each file with switch data
        for idx, ii in enumerate(self.rummage_through()):
            try:
                # Get data from switch file
                data_dic = self.read_excel_data_file(ii)
            except ValueError as E:
                print(E)
            # Add switch data to sql table
            self.add_switch_data_to_table(conn, data_dic)

        conn.commit()
        conn.close()

        return

    @staticmethod
    def add_switch_data_to_table(conn, dic):
        """Append switch data to SQL table.

            Parameters:
                conn: Connection to SQL table
                dic: Dictionary with data with keys ['Downstroke', 'Upstroke'] and
                values dataframe with columns ['force', 'displacement', 'switch_name', 'mode'].
            """
        for kk, df in dic.items():
            print('Doing {} for {}'.format(df['switch_name'][0], df['mode'][0]))
            df.to_sql('force_curves', conn, if_exists='append', index=False)

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
        df = pd.read_excel(file_path, header=None, usecols='B', skiprows=1,
                           sheet_name=['DataTable'])
        switch_name = df['DataTable'].iloc[0, 0]

        # Get dictionary with data from Excel. Keys are Downstroke, Upstroke
        # and columns are 2 (force) and 11 (displacement).
        data_dic = pd.read_excel(file_path, header=None, usecols='C,L',
                                 skiprows=5, sheet_name=['Downstroke', 'Upstroke'])

        # Rename columns and add switch name and mode to the df
        for kk, _df in data_dic.items():
            _df.rename(columns={2: 'Force', 11: 'Displacement'}, inplace=True)
            _df['switch_name'] = switch_name
            _df['mode'] = kk

        return data_dic

    def create_table(self):
        """Create SQL table."""
        conn, cur = self.create_conn()

        cur.execute(""" DROP TABLE IF EXISTS force_curves """)

        _sql = """ CREATE TABLE force_curves(
                    force CHAR(100),
                    displacement CHAR(100),
                    switch_name CHAR(100),
                    mode CHAR(100))
                    """

        cur.execute(_sql)
        cur.close()
        conn.close()

    @staticmethod
    def create_conn():
        """Return connection and cursor of the SQL table.

            Parameters:
            Returns:
                Tuple with SQL connection and cursor
        """
        conn = None
        try:
            conn = sqlite3.connect('force_curves')
            return conn, conn.cursor()
        except Exception as E:
            print(E)

        return

    def rummage_through(self) -> list[str]:
        """Return a list with the file paths of all switch data files.

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
        """Return a list with the file paths of switch data in the specific directory.

        Parameters:
            switch_dir: Name of directory for the specific switch
        Returns:
            List with file paths with switch data in the directory
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

        Parameters:
        Returns:
                List with the directories of all switches
            """
        directory_names = [ii[0] for ii in os.walk('../')]
        # Remove hidden directories and current directory
        directory_names = [ii for ii in directory_names if (
                not ii.startswith('../.') and not ii.startswith('../0_data'))]

        return directory_names[1:]

