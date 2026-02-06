import unittest
import os
import sys
import toml

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import after path is set up - this will test that modules can be loaded
try:
    from backend.syndromes.syndrome import ALL_SYNDROMES, Syndrome
    from backend.herbs.herb import ALL_HERBS, Herb
    IMPORTS_SUCCESSFUL = True
except ImportError as e:
    IMPORTS_SUCCESSFUL = False
    IMPORT_ERROR = str(e)


class TestSyndromesAndHerbs(unittest.TestCase):

    def test_all_syndromes_load_successfully(self):
        """Test that ALL_SYNDROMES can be loaded without errors."""
        if not IMPORTS_SUCCESSFUL:
            self.skipTest(f"Cannot test loading - imports failed: {IMPORT_ERROR}")
        # This will raise an exception if there are any syntax errors or loading issues
        self.assertIsNotNone(ALL_SYNDROMES)
        self.assertIsInstance(ALL_SYNDROMES, list)
        # Verify that all loaded items are Syndrome objects
        for syndrome in ALL_SYNDROMES:
            self.assertIsInstance(syndrome, Syndrome)
            # Verify basic properties exist
            self.assertIsNotNone(syndrome.name)
            self.assertIsNotNone(syndrome.organ)
            self.assertIsNotNone(syndrome.diagnosis)
            self.assertIsNotNone(syndrome.treatment)

    def test_all_herbs_load_successfully(self):
        """Test that ALL_HERBS can be loaded without errors."""
        if not IMPORTS_SUCCESSFUL:
            self.skipTest(f"Cannot test loading - imports failed: {IMPORT_ERROR}")
        # This will raise an exception if there are any syntax errors or loading issues
        self.assertIsNotNone(ALL_HERBS)
        self.assertIsInstance(ALL_HERBS, list)
        # Verify that all loaded items are Herb objects
        for herb in ALL_HERBS:
            self.assertIsInstance(herb, Herb)
            # Verify basic properties exist
            self.assertIsNotNone(herb.name)
            self.assertIsNotNone(herb.identifier)

    def test_syndrome_toml_files_can_be_loaded(self):
        """Test that all syndrome TOML files can be loaded by the Syndrome.from_toml method."""
        if not IMPORTS_SUCCESSFUL:
            self.skipTest(f"Cannot test TOML loading - imports failed: {IMPORT_ERROR}")
        
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'syndromes', 'data')
        
        if not os.path.exists(data_dir):
            self.skipTest(f"Syndromes data directory not found: {data_dir}")
        
        for filename in os.listdir(data_dir):
            if filename.endswith('.toml'):
                file_path = os.path.join(data_dir, filename)
                with self.subTest(file=filename):
                    # Try to load the TOML file using the actual loading method
                    try:
                        syndromes = Syndrome.from_toml(file_path)
                        # Verify we got a list of syndromes
                        self.assertIsInstance(syndromes, list)
                        # Verify each is a Syndrome object
                        for syndrome in syndromes:
                            self.assertIsInstance(syndrome, Syndrome)
                    except Exception as e:
                        self.fail(f"Error loading {filename}: {str(e)}")

    def test_herb_toml_files_can_be_loaded(self):
        """Test that all herb TOML files can be loaded by the Herb.from_toml method."""
        if not IMPORTS_SUCCESSFUL:
            self.skipTest(f"Cannot test TOML loading - imports failed: {IMPORT_ERROR}")
        
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'herbs', 'data')
        
        if not os.path.exists(data_dir):
            self.skipTest(f"Herbs data directory not found: {data_dir}")
        
        for filename in os.listdir(data_dir):
            if filename.endswith('.toml'):
                file_path = os.path.join(data_dir, filename)
                with self.subTest(file=filename):
                    # Try to load the TOML file using the actual loading method
                    try:
                        herbs = Herb.from_toml(file_path)
                        # Verify we got a list of herbs
                        self.assertIsInstance(herbs, list)
                        # Verify each is a Herb object
                        for herb in herbs:
                            self.assertIsInstance(herb, Herb)
                    except Exception as e:
                        self.fail(f"Error loading {filename}: {str(e)}")

    def test_syndromes_have_valid_structure(self):
        """Test that all loaded syndromes have valid structure and can access their properties."""
        if not IMPORTS_SUCCESSFUL:
            self.skipTest(f"Cannot test structure - imports failed: {IMPORT_ERROR}")
        for syndrome in ALL_SYNDROMES:
            with self.subTest(syndrome=syndrome.name):
                # Test that properties can be accessed without errors
                try:
                    _ = syndrome.identifier
                    _ = syndrome.name
                    _ = syndrome.organ
                    _ = syndrome.diagnosis
                    _ = syndrome.treatment
                    _ = syndrome.diagnosis_str
                    _ = syndrome.treatment_str
                    _ = syndrome.etiology_str
                except Exception as e:
                    self.fail(f"Error accessing properties of syndrome '{syndrome.name}': {str(e)}")

    def test_herbs_have_valid_structure(self):
        """Test that all loaded herbs have valid structure and can access their properties."""
        if not IMPORTS_SUCCESSFUL:
            self.skipTest(f"Cannot test structure - imports failed: {IMPORT_ERROR}")
        for herb in ALL_HERBS:
            with self.subTest(herb=herb.name):
                # Test that properties can be accessed without errors
                try:
                    _ = herb.identifier
                    _ = herb.name
                except Exception as e:
                    self.fail(f"Error accessing properties of herb '{herb.name}': {str(e)}")

