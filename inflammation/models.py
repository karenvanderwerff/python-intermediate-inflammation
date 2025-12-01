"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains
inflammation data for a single patient taken over a number of days
and each column represents a single day across all patients.
"""

import numpy as np
import json


def load_csv(filename: str) -> np.ndarray:
    """Load a Numpy array from csv

    Parameters
    ----------
    filename : str
        path to the csv file

    Returns
    -------
    np.ndarray
        2D array of inflammation data
    """
    return np.loadtxt(fname=filename, delimiter=",")


def load_json(filename):
    """Load a numpy array from a JSON document.

    Expected format:
    [
      {
        "observations": [0, 1]
      },
      {
        "observations": [0, 2]
      }
    ]
    :param filename: Filename of CSV to load
    """
    with open(filename, "r", encoding="utf-8") as file:
        data_as_json = json.load(file)
        return [np.array(entry["observations"]) for entry in data_as_json]


def daily_mean(data):
    """Calculate the daily mean of a 2d inflammation data array.

    :param data: np array
    :returns: average per column
    """
    return np.mean(data, axis=0)


def daily_max(data):
    """Calculate the daily max of a 2d inflammation data array.

    :param data: np array
    :returns: max value per column
    """
    return np.max(data, axis=0)


def daily_min(data):
    """Calculate the daily min of a 2d inflammation data array.

    :param data: np array
    :returns: min value per column
    """
    return np.min(data, axis=0)


def patient_normalise(data):
    """
    Normalise patient data from a 2D inflammation data array.

    NaN values are ignored, and normalised to 0.

    Negative values are rounded to 0.
    """
    # Check if data is an ndarray
    if not isinstance(data, np.ndarray):
        raise TypeError("Input data should be an ndarray")
    # Check for correct shape
    if len(data.shape) != 2:
        raise ValueError("Inflammation array should be 2-dimensional")
    # Ensure non-negative values only
    if np.any(data < 0):
        raise ValueError("Inflammation values should not be negative")
    max_data = np.nanmax(data, axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        normalised = data / max_data[:, np.newaxis]
    normalised[np.isnan(normalised)] = 0
    return normalised


def analyse_data(data_source):
    """Calculates the standard deviation by day between datasets.
    Works out the mean inflammation value for each day across all datasets,
    then plots the graphs of standard deviation of these means.
    """
    data = data_source.load_inflammation_data()
    daily_standard_deviation = compute_standard_deviation_by_day(data)

    return daily_standard_deviation


def compute_standard_deviation_by_day(data):
    means_by_day = map(daily_mean, data)
    means_by_day_matrix = np.stack(list(means_by_day))

    daily_standard_deviation = np.std(means_by_day_matrix, axis=0)
    return daily_standard_deviation
