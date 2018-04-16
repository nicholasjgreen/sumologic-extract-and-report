import unittest


def myfunction(str):
    return len(str)


class MyFirstTest(unittest.TestCase):
    """My first ones in python, at least"""
    
    def setUp(self):
        """Fixture setup"""
        self.data = "hello world"
        
    def tearDown(self):
        """Fixture clean up"""
        self.data = None
    
    def test_myfunction(self):
        """Basic smoke"""
        myfunction(self.data)

    def test_len(self):
        l = myfunction(self.data)
        self.assertEqual(l, 11, 'String should be 11 long')

    def test_invalidargs(self):
        """Check for proper exception"""
        with self.assertRaises(TypeError):
            myfunction(None)
        with self.assertRaises(TypeError):
            myfunction(42)
        
if __name__ == "__main__":
    unittest.main()
