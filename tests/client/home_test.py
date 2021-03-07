import unittest 
from dearpygui.simple import window
from dearpygui.core import add_text, start_dearpygui

class TestHome(unittest.TestCase):
    """test vision toolkit GUI
    """        

    def test_main_window(self) -> None:
        """
        test main loop correctness
        """ 
        with window('Vision 5 Toolkit'):
            add_text('this is some text')

        self.assertIsNotNone(start_dearpygui())
        start_dearpygui(primary_window="Vision 5 Toolkit")


if __name__=="__main__":
    unittest.main()