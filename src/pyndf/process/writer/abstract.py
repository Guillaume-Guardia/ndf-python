# -*- coding: utf-8 -*-

import os
from pyndf.qtlib import QtCore
from pyndf.logbook import Logger


class AbstractWriter(Logger, QtCore.QObject):
    """Abstract class for write file."""

    ext = None

    def __init__(self, filename=None, dir=None, ext=None, **kwargs):
        """Initialisation

        Args:
            filename (string, optional): file to read. Defaults to None.
            sheet_name (int or string, optional): Sheet to read. Defaults to 0 -> First Sheet.
            regex_libelle (str, optional): Regex. Defaults to "INDEMNITE.*".
        """
        super().__init__(**kwargs)
        self.filename = filename
        self.dir = dir

    def create_path(self, filename, dir=None, ext=None, force=True):
        """Check path method.

        Args:
            filename (string): just the basename of the wanted file
            dir (str): directory to the futur new file.
            ext (str): extension of the file added to filename
            force (bool, optional): Force the creation of file. Defaults to True.

        Raises:
            FileExistsError: If force is deactivate, raise the error if the filename already exists.

        Returns:
            string: Path of the new file
        """

        filename = filename or self.filename

        if filename is None:
            raise Exception("No filename provided !")

        dir = dir or self.dir
        ext = ext or self.ext

        if dir is not None and os.path.exists(dir):
            # Modify or Add dir to filename
            path = os.path.join(dir, os.path.basename(filename))

        if ext is not None and ext.startswith("."):
            # Add extension of filename
            path = path.split(".")[0] + ext

        # Check if the file exists
        if os.path.exists(path) and not force:
            raise FileExistsError

        self.log.info(f"Write data in file {os.path.basename(path)}")
        return path
