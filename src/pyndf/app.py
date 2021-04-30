import os
import re
import yaml
import pandas as pd
from PyQt6 import QtWidgets, QtCore
from pyndf.google_maps_process import DistanceMatrixAPI
from pyndf.logbook import Logger


# Main program of the app
class Window(QtWidgets.QWidget, Logger):
    def __init__(self):
        super().__init__()

        # configuration file
        conf_file = os.path.join(os.path.dirname(__file__), "conf", "conf.yaml")

        with open(conf_file, "rt", encoding="utf-8") as opened_file:
            self.configuration = yaml.safe_load(opened_file)

        self.threadpool = QtCore.QThreadPool()

        # En entrée, feuille excel
        self.sourcefile_x = QtWidgets.QLineEdit()
        self.sourcefile_x.setDisabled(True)  # must use the file finder to select a valid file.

        self.file_select_x = QtWidgets.QPushButton("Select Excel...")
        self.file_select_x.pressed.connect(self.choose_exl_file)

        # En sortie, répertoire de sortie
        self.output = QtWidgets.QLineEdit()
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
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select a file", filter="Excel files (*.xl*)")
        if filename:
            self.sourcefile_x.setText(filename)

    def choose_output_file(self):
        output = QtWidgets.QFileDialog.getExistingDirectory(self, "Select a folder")
        if output:
            self.output.setText(output)

    def generate(self):
        if not self.sourcefile_x.text():
            return  # If the field is empty, ignore.

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

    def process(self, data):
        api = DistanceMatrixAPI(self.configuration)
        # Open the window, set the file to upload, button to generate NDF
        xl_file = data["sourcefile_x"]
        dataframe = pd.read_excel(xl_file, sheet_name="A")

        # Recuperer les colonnes et les placer dans un dico
        try:
            reg = re.compile("INDEMNITE.*")
            for index, record in enumerate(dataframe.to_dict("records")):
                my_record = {}

                if reg.match(record[self.configuration["colonne"]["libelle"]]) is None:
                    continue

                for key in (
                    "nom",
                    "matricule",
                    "societe",
                    "agence",
                    "agence_o",
                    "periode_paie",
                    "client",
                    "adresse_client",
                    "adresse_intervenant",
                    "quantite_payee",
                    "prix_unitaire",
                    "total",
                ):
                    my_record[key] = record[self.configuration["colonne"][key]]
                    self.log.info(my_record[key])

                distance, duration = api.run(my_record["adresse_client"], my_record["adresse_intervenant"])

                # Col Nombre de km par mois
                my_record["nbrkm_mois"] = my_record["quantite_payee"] * 2 * distance

                # Forfait
                my_record["forfait"] = my_record["total"] / my_record["nbrkm_mois"]

                # Create pdf facture
                
                self.log.info(f"{index}: {my_record}")
        except Exception as error:
            self.log.exception(error)
        else:
            self.generated()

    def generated(self):
        self.generate_btn.setDisabled(False)
        QtWidgets.QMessageBox.information(self, "Finished", "PDFs have been generated")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = Window()
    w.show()
    app.exec()
