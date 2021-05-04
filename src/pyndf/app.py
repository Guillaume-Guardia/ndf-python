# -*- coding: utf-8 -*-

import os
import re
from collections import defaultdict
import yaml
import pandas as pd
from PyQt6 import QtWidgets, QtCore
from pyndf.google_maps_process import DistanceMatrixAPI
from pyndf.ndf_template import NdfTemplate
from pyndf.logbook import Logger


class Window(Logger, QtWidgets.QWidget):
    """Main window of the app

    Args:
        QtWidgets (Qobject): Qt object
        Logger (object): For logging
    """

    def __init__(self):
        super().__init__()

        # configuration file
        conf_file = os.path.join(os.path.dirname(__file__), "conf", "conf.yaml")

        with open(conf_file, "rt", encoding="utf-8") as opened_file:
            self.configuration = yaml.safe_load(opened_file)

        self.threadpool = QtCore.QThreadPool()

        # En entrée, feuille excel
        self.sourcefile_x = QtWidgets.QLineEdit()
        self.sourcefile_x.setText(r"C:\Users\guill\Documents\Projets\NDF_python\venv\src\ndf-python\data\test.xlsx")
        self.sourcefile_x.setDisabled(True)  # must use the file finder to select a valid file.

        self.file_select_x = QtWidgets.QPushButton("Select Excel...")
        self.file_select_x.pressed.connect(self.choose_exl_file)

        # En sortie, répertoire de sortie
        self.output = QtWidgets.QLineEdit()
        self.output.setText(r"C:\Users\guill\Documents\Projets\NDF_python\venv\src\output")
        self.output.setDisabled(True)  # must use the file finder to select a valid file.

        self.file_select_output = QtWidgets.QPushButton("Select output...")
        self.file_select_output.pressed.connect(self.choose_output_file)

        self.generate_btn = QtWidgets.QPushButton("Generate PDF")
        self.generate_btn.pressed.connect(self.generate)

        layout = QtWidgets.QFormLayout()
        layout.addRow(self.sourcefile_x, self.file_select_x)
        layout.addRow(self.output, self.file_select_output)
        layout.addRow(self.generate_btn)

        self.setLayout(layout)

    def choose_exl_file(self):
        """Method which call the native file dialog to choose excel file."""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select a file", filter="Excel files (*.xl*)")
        if filename:
            self.sourcefile_x.setText(filename)

    def choose_output_file(self):
        """Method which call the native file dialog to choose the output directory."""
        output = QtWidgets.QFileDialog.getExistingDirectory(self, "Select a folder")
        if output:
            self.output.setText(output)

    def generate(self):
        """Method triggered with the button to start the generation of pdf.

        Returns:
            [type]: [description]
        """
        if not self.sourcefile_x.text():
            return None  # If the field is empty, ignore.

        self.generate_btn.setDisabled(True)

        data = {
            "sourcefile_x": self.sourcefile_x.text(),
            "output": self.output.text(),
        }
        self.process(data)
        # g = Generator(data)
        # g.signals.finished.connect(self.generated)
        # g.signals.error.connect(print)  # Print errors to console.
        # self.threadpool.start(g)
        return True

    def process(self, data):
        """Process method

        Args:
            data (dict): two info: excel file + output directory
        """
        api = DistanceMatrixAPI(self.configuration)
        template = NdfTemplate(directory=data.get("output", "."))
        # Open the window, set the file to upload, button to generate NDF
        xl_file = data["sourcefile_x"]
        dataframe = pd.read_excel(xl_file, sheet_name="A")

        records = defaultdict(dict)

        # Recuperer les colonnes et les placer dans un dico
        try:
            reg = re.compile("INDEMNITE.*")
            for record in dataframe.to_dict("records"):
                matricule = record[self.configuration["colonne"]["matricule"]]

                if reg.match(record[self.configuration["colonne"]["libelle"]]) is None:
                    continue

                if matricule not in records:
                    # Personal info
                    for key in ("nom", "matricule", "societe", "agence", "agence_o", "adresse_intervenant"):
                        records[matricule][key] = record[self.configuration["colonne"][key]]
                        self.log.debug(f"{matricule} | {key} = {records[matricule][key]}")
                    records[matricule]["missions"] = []

                # Mission Info
                mission_record = {}
                for key in (
                    "periode_production",
                    "client",
                    "adresse_client",
                    "quantite_payee",
                    "prix_unitaire",
                    "total",
                ):
                    mission_record[key] = record[self.configuration["colonne"][key]]
                    self.log.debug(f"{matricule} | missions | {key} = {mission_record[key]}")
                records[matricule]["missions"].append(mission_record)

                distance, duration = api.run(
                    records[matricule]["missions"][-1]["adresse_client"], records[matricule]["adresse_intervenant"]
                )
                self.log.debug(f'Origin: {records[matricule]["missions"][-1]["adresse_client"]}')
                self.log.debug(f'Destination: {records[matricule]["adresse_intervenant"]}')
                self.log.debug(f"Distance: {distance}, duration: {duration}")

                # Col Nombre de km par mois
                records[matricule]["missions"][-1]["nbrkm_mois"] = (
                    records[matricule]["missions"][-1]["quantite_payee"] * 2 * distance
                )

                # Forfait
                records[matricule]["missions"][-1]["forfait"] = (
                    records[matricule]["missions"][-1]["total"] / records[matricule]["missions"][-1]["nbrkm_mois"]
                )

            for matricule, data in records.items():
                self.log.info(f"Start Create pdf for matricule {matricule} with {len(data['missions'])} missions.")
                # Create pdf facture
                template.create(data)

        except Exception as error:
            self.log.exception(error)
        else:
            self.generated()

    def generated(self):
        """Success methdod"""
        self.generate_btn.setDisabled(False)
        QtWidgets.QMessageBox.information(self, "Finished", "PDFs have been generated")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = Window()
    w.show()
    app.exec()
