#/usr/bin/env python


# CSV handler for block model loading/saving
class CSVHandler:
    def __init__(self):
        pass

    # Loads a CSV file and updates the model
    def load_blockmodel(self, model, filepath: str) -> bool:
        # TODO Read file on filepath
        # TODO Get positions and data of block model
        # TODO Update the model
        return False

    # Saves a CSV file and updates the model
    def save_blockmodel(self, filepath: str) -> bool:
        # TODO Create a new file on filepath
        # TODO Write the DXF with the model's vertices and faces (dxfgrabber?)
        # TODO Close the file
        return False
