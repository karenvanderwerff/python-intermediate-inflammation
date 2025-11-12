"""Module containing mechanism for calculating standard deviation between datasets.
"""

import glob
import os
import numpy as np

from inflammation import models, views


class CSVDataSource:
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def load_inflammation_data(self):
        data_file_paths = glob.glob(os.path.join(self.dir_path, 'inflammation*.csv'))
        if len(data_file_paths) == 0:
            raise ValueError(f"No inflammation data CSV files found in path {self.dir_path}")
        data = map(models.load_csv, data_file_paths)
        return list(data)


class JSONDataSource:
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def load_json(self):
        data_file_paths = glob.glob(os.path.join(self.dir_path, 'inflammation*.json'))
        if len(data_file_paths) == 0:
            raise ValueError(f"No inflammation JSON files found in path {self.dir_path}")
        data = map(models.load_json, data_file_paths)
        return list(data)


def load_inflammation_data(data_dir):
    """Loads inflammation data from CSV files within the given directory.

    :param data_dir: Directory to be searched for inflammation CSV files.
    :returns: List of 2D NumPy arrays with inflammation data from all CSV files.
    """
    data_file_paths = glob.glob(os.path.join(data_dir, 'inflammation*.csv'))
    if len(data_file_paths) == 0:
        raise ValueError(f"No inflammation data CSV files found in path {data_dir}")
    data = map(models.load_csv, data_file_paths)
    return list(data)


def analyse_data(data_source):
    """Calculates the standard deviation by day between datasets.

    Works out the mean inflammation value for each day across all datasets,
    then plots the graphs of standard deviation of these means.
    
    :param data_dir: Directory that contains the inflammation CSV files.
    """
    data = data_source.load_inflammation_data()

    means_by_day = map(models.daily_mean, data)
    means_by_day_matrix = np.stack(list(means_by_day))

    daily_standard_deviation = np.std(means_by_day_matrix, axis=0)

    graph_data = {
        'standard deviation by day': daily_standard_deviation,
    }
    views.visualize(graph_data)