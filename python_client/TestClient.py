import unittest
from Client import Client
class TestClient(unittest.TestCase):

    def setUp(self):
        self.c = Client()

    def test_results_output(self):
        #TODO: figure out how to test this
        graph_data = {
            "dates":['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            "data":[{
                            "name": 'Group 3',
                            "data": [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
                        }, {
                            "name": 'Group 9',
                            "data": [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]
                        }, {
                            "name": 'Group 22',
                            "data": [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
            }],
            "y_axis_legend": 'Temperature (\u00b0C)',
            "title":'Temperature',
            "subtitle":'Source: Collection 3 Data',
            "data_type": '(\u00b0C)'}
        self.c.generate_graphs(**graph_data)
        self.c.generate_graphs(open_browser=True,**graph_data)


    # These require a sensor connected to run
    """
    def test_data_capture_return(self):
        output = self.c.capture_data(2)
        self.assertTrue(output.count(",") == 2*output.count("\n"))

    def test_data_capture_write(self):
        self.c.capture_data(2,False,True,"data.csv")
        contents = "";
        with open("data.csv") as f:
            for line in f:
                if line.strip() != "":
                    self.assertTrue(line.count(",") == 2)
    """

if __name__ == '__main__':
    unittest.main()
