#!/usr/bin/env python3
"""Software for managing and analysing patients' inflammation data in our imaginary hospital."""

import argparse
import os

from inflammation import models, views
from inflammation.compute_data import analyse_data, CSVDataSource, JSONDataSource


def main(args):
    """The MVC Controller of the patient inflammation data system.

    The Controller is responsible for:
    - selecting the necessary models and views for the current task
    - passing data between models and views
    """
    InFiles = args.infiles
    if not isinstance(InFiles, list):
        InFiles = [args.infiles]


    if args.full_data_analysis:
        extensions = {os.path.splitext(f)[1] for f in os.listdir(InFiles[0]) if os.path.isfile(os.path.join(InFiles[0], f))}
        # _, extension = os.path.splitext(InFiles[0])
        # if extension == '.json':
        if '.json' in extensions:
            data_source = JSONDataSource(os.path.dirname(InFiles[0]))
        # elif extension == '.csv':
        if '.csv' in extensions:
            data_source = CSVDataSource(os.path.dirname(InFiles[0]))
        else:
            raise ValueError(f'Unsupported data file format: {extension}')
        analyse_data(data_source)
        return

    for filename in InFiles:
        inflammation_data = models.load_csv(filename)

        view_data = {
            'average': models.daily_mean(inflammation_data),
            'max': models.daily_max(inflammation_data),
            'min': models.daily_min(inflammation_data)
        }

        views.visualize(view_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A basic patient inflammation data management system')

    parser.add_argument(
        'infiles',
        nargs='+',
        help='Input CSV(s) containing inflammation series for each patient')

    parser.add_argument(
        '--full-data-analysis',
        action='store_true',
        dest='full_data_analysis')

    args = parser.parse_args()

    main(args)
