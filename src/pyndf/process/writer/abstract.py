# -*- coding: utf-8 -*-

import os
from pyndf.constants import CONST
from pyndf.qtlib import QtCore
from pyndf.logbook import Logger, log_time
from pyndf.utils import Utils


class AbstractWriter(Logger, QtCore.QObject):
    """Abstract class for write file."""

    ext = None
    suffixe = "-pyndf"

    def __init__(self, *args, directory=None, overwrite=True, **kwargs):
        """Initialisation"""
        super().__init__(*args, **kwargs)
        self.directory = directory
        self.overwrite = overwrite

    def create_path(self, filename, directory=None, page: int = None, ext=None, force=False):
        """Check path method.

        Args:
            filename (string): just the basename of the wanted file
            directory (str): directory to the futur new file.
            ext (str): extension of the file added to filename
            force (bool, optional): Force the creation of file. Defaults to True.

        Raises:
            FileExistsError: If force is deactivate, raise the error if the filename already exists.

        Returns:
            string: Path of the new file
        """

        path = filename or self.filename

        if path is None:
            raise Exception("No filename provided !")

        directory = directory or self.directory
        ext = ext or self.ext

        if directory is not None and os.path.exists(directory):
            # Modify or Add directory to filename
            path = os.path.join(directory, os.path.basename(path))

        if ext is not None and ext.startswith("."):
            # Add extension of filename
            path = path.split(".")[0] + ext

        if page is not None:
            path = Utils.insert(path, path.index("."), f"_page-{page}")

        if self.suffixe is not None and self.suffixe not in path:
            path = Utils.insert(path, path.index("."), self.suffixe)

        # Check if the file exists
        force = force or self.overwrite
        if os.path.exists(path) and not force:
            raise FileExistsError

        self.log.info(f"Write data in file {os.path.basename(path)}")
        return path

    @log_time
    def write(self, data, filename=None):
        """Create method, add each element of pdf.

        Args:
            data (dict): record data with personnal info of collaborator and his missions info.
        """
        try:
            filename = self.create_path(filename)
            status = self._write(data, filename)

        except FileExistsError:
            filename = self.create_path(filename, force=True)
            status = CONST.STATUS.FILE_ALREADY_EXISTS

        except Exception as e:
            self.log.exception(e)
            status = CONST.STATUS.ERROR

        return filename, status
