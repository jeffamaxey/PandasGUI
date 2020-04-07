"""DataFrameExplorer"""

from PyQt5 import QtWidgets
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from pandasgui.widgets import DataFrameViewer
from pandasgui.widgets import FigureViewer
import traceback

class DataFrameExplorer(QtWidgets.QTabWidget):
    """
    This is a QTabWidget for analyzing a single DataFrame where the first tab is a DataFrameViewer widget

    Args:
        df (DataFrame): The DataFrame to display
    """

    def __init__(self, df):

        super().__init__()

        df = df.copy()
        self.df = df

        # DataFrame tab
        self.dataframe_tab = DataFrameViewer(self.df)
        self.addTab(self.dataframe_tab, "DataFrame")

        # Statistics tab
        try:
            self.statistics_tab = self.make_statistics_tab(df)
            self.addTab(self.statistics_tab, "Statistics")
        except:
            traceback.print_exc()

        # Histogram tab
        try:
            if not (type(df.index) == pd.MultiIndex or type(df.columns) == pd.MultiIndex):
                histogram_tab = self.make_histogram_tab(df)
                self.addTab(histogram_tab, "Histogram")
        except:
            traceback.print_exc()

    def make_statistics_tab(self, df):
        stats_df = pd.DataFrame({
            'Type': df.dtypes.replace('object', 'string'),
            'Count': df.count(),
            'Mean': df.mean(numeric_only=True),
            'StdDev': df.std(numeric_only=True),
            'Min': df.min(numeric_only=True),
            'Max': df.max(numeric_only=True),
        })
        w = DataFrameViewer(stats_df)
        w.setAutoFillBackground(True)
        return w


# Examples
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    from pandasgui.datasets import iris, flights, multi, pokemon

    # Create and show widget
    dfe = DataFrameExplorer(flights)
    dfe.show()

    sys.exit(app.exec_())
