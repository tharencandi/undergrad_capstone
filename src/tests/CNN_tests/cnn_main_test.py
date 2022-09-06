import pytest 
from src.CNN.cnn_main import main
import sys
def test_no_command_line_args():
    """Test whether arguments from the command line are set up correctly in a HermesApp object."""
    sys.argv = ["some_name"]
    
    main()
    out, err = pytest.capfd.readouterr()
    assert out == "\nincorrect use.\npython3 dataset.py (train | test) (NBL | NBD_SN) relative_folder_location"

    