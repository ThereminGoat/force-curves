import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict

class DataPlot:

    def __init__(self):
        self.conn, self.cur = self.connect_db()
        self.switch_dic = self.all_switches_dic()

    def plot_switches(self):

        fig, ax = plt.subplots(nrows=2, ncols=1, dpi=100, figsize=(8, 12))
        legend_cols = ["#648ace", "#c2843c", "#ab62c0", "#6ca659", "#ca556a"]
        switch_id_todo = [19, 221, 4, 601, 398]

        for idx0, mode in enumerate(['Downstroke', 'Upstroke']):
            for idx1, ii in enumerate(switch_id_todo):
                switch_data = self.get_switch_data(ii, mode)

                ax[idx0].plot(switch_data[:, 1], switch_data[:, 0], color=legend_cols[idx1],
                              lw=2)

            figure_switches_names = [self.switch_dic[ii] for ii in switch_id_todo]
            self.work_figure(ax[idx0], figure_switches_names, mode)

    @staticmethod
    def work_figure(ax, figure_switches_names, mode):
        """Works on the figure.

            Parameters:
                ax: Figure axis
                figure_switches_names: List with names of the plotted switches
                mode: Downstroke/Upstroke

            Returns:
        """
        ax.set_xlabel('Displacement (mm)', fontsize=13)
        ax.set_ylabel('Force', fontsize=13)
        ax.set_title('Force Curves, {}'.format(mode), fontsize=14)
        ax.set_xlim([-.2, 4])
        ax.set_ylim([0, 200])

        if mode == 'Upstroke':
            ax.invert_xaxis()
        else:
            ax.legend(figure_switches_names)

        return

    def get_switch_data(self, idx: int, mode: str) -> np.ndarray:
        """Return array with force and displacement data for the particular switch
            and mode.

            Parameters:
                idx: switch id
                mode: 'Downstroke'/'Upstroke'

            Return:
                Array with force and displacement data for the switch to be plotted
            """
        _query = """SELECT force, displacement
                    FROM force_curves
                    WHERE switch_name = ? AND mode = ?"""
        self.cur.execute(_query, (self.switch_dic[idx], mode,))
        rows = self.cur.fetchall()
        # Array in db is string, convert to float
        arr = np.array(np.asarray(rows), dtype=float)
        return arr

    def all_switches_dic(self) -> dict[int, str]:
        """Return dictionary with keys an id and values the name of the 
            switch for all switches.

            Parameters:
            Returns:
                Dictionary with keys the index, and values the name of the switch
            """
        switch_names = self.get_all_switch_names()
        # Index for the switches
        idx = list(range(1, len(switch_names) + 1))
        dic = {kk: vv for kk, vv in zip(idx, switch_names)}

        return dic

    def get_all_switch_names(self):

        _query = 'SELECT DISTINCT(switch_name) FROM force_curves'
        df = pd.read_sql_query(_query, self.conn)

        switch_names_list = list(df.iloc[:, 0])

        return switch_names_list

    @staticmethod
    def connect_db():
        """Return connection and cursor of the SQL table.

            Parameters:
            Returns:
                Tuple with SQL connection and cursor
        """
        if os.path.isfile('./force_curves'):
            conn = sqlite3.connect('./force_curves')
            return conn, conn.cursor()
        else:
            print('Could not find db, do not bother')

        return