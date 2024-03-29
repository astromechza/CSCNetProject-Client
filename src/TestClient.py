import unittest
from Client import Client
import os
graph_data = {
    "dates":[1365593877.034777, 1365593877.034778, 1365593877.034778, 1365593877.034778, 1365593877.034779, 1365593877.034779, 1365593877.03478, 1365593877.03478, 1365593877.03478, 1365593877.034781, 1365593877.034781, 1365593877.034781],
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

results_data = [{u'group_id': 1,
u'type': u'light', u'value': 1, u'time': u'2013-04-01 00:00:00.0'},
{u'group_id': 1, u'type': u'light', u'value': 2, u'time': u'2013-04-01 00:00:00.0'}, {u'group_id': 1, u'type': u'light', u'value': 3, u'time': u'2013-04-01 00:00:00.0'}, {u'group_id': 1, u'type': u'light', u'value': 1, u'time': u'2013-04-01 00:00:00.0'}, {u'group_id': 1, u'type': u'light',u'value': 8, u'time': u'2013-04-01 00:00:00.0'}, {u'group_id': 1, u'type':u'humidity', u'value': 61.5658, u'time': u'2013-04-08 16:55:35.0'},{u'group_id': 1, u'type': u'light', u'value': 12.1676, u'time': u'2013-04-08 16:55:36.0'}, {u'group_id': 1, u'type': u'humidity', u'value': 67.8501,u'time': u'2013-04-08 16:55:36.0'}, {u'group_id': 1, u'type': u'humidity',u'value': 64.3722, u'time': u'2013-04-08 16:55:37.0'}, {u'group_id': 1,u'type': u'humidity', u'value': 51.9798, u'time': u'2013-04-08 16:55:37.0'},{u'group_id': 1, u'type': u'humidity', u'value': 14.6104, u'time': u'2013-04-08 16:55:38.0'}, {u'group_id': 1, u'type': u'light', u'value': 59.1693, u'time':u'2013-04-08 16:55:38.0'}, {u'group_id': 1, u'type': u'light', u'value':34.8685, u'time': u'2013-04-08 16:55:40.0'}, {u'group_id': 1, u'type':u'humidity', u'value': 26.1523, u'time': u'2013-04-08 16:55:41.0'},{u'group_id': 1, u'type': u'light', u'value': 32.1843, u'time': u'2013-04-08 16:55:42.0'}, {u'group_id': 1, u'type': u'light', u'value': 18.2174, u'time':u'2013-04-08 16:55:42.0'}, {u'group_id': 1, u'type': u'light', u'value':69.6449, u'time': u'2013-04-08 16:55:43.0'}, {u'group_id': 1, u'type':u'light', u'value': 5.55437, u'time': u'2013-04-08 16:55:43.0'}]
class TestClient(unittest.TestCase):

    def setUp(self):
        self.c = Client()

    def validate_results(self):
        """Validates that the results file given is a valid set of results"""
        # TODO: Make this a lot more more comprehensive than just checking if a
        # file exists
        self.assertTrue(os.path.isfile("results.html"))

    def test_results_output(self):
        """Test if client renders a graph"""
        self.c.generate_graphs(data=[graph_data],feedback=False)
        self.validate_results()
    
    def test_results_multiple_output(self):
        """Test if client renders a graph more than one graph on a page"""
        self.c.generate_graphs(data=[graph_data,graph_data],feedback=False)
        self.validate_results()
    
    def test_generate_graphs_from_results(self):
        """Test if client can render graph from server results"""
        self.c.generate_graph_from_results(results_data)
        self.validate_results()

    def test_generating_graph_from_local(self):
        """Tests if client can rendering graphs from a local file"""
        # Test if render works for sensor data capture
        self.c.generate_graph_from_data_file("data/test_data.csv",feedback=False);
        self.validate_results()
        # Test if render works for server download
        self.c.generate_graph_from_data_file("data/test_data_server.csv",feedback=False);
        self.validate_results()

    def test_ping(self):
        """Tests if client can reach server"""
        self.assertTrue(self.c.ping_server()["result"]=="pong")
    
    def test_download(self):
        """Tests if client can download data from server"""
        self.assertTrue(self.c.download(group_ids=[3])["result"])

    def test_multiple_group_downloads(self):
        """Tests if client can download  data with multiple group ids from
        server"""
        self.assertTrue(self.c.download(group_ids=[1,3])["result"])

    def test_download_logs(self):
        """Tests if client can download logs from the server"""
        self.assertTrue(self.c.get_logs()["result"]["lines"])
    # Don't want to fill the server with repeated data
    """
    def test_upload(self):
        with open("data/test_data.csv") as f:
            self.c.upload("".join(f.readlines()))
    """

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
