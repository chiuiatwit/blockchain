import unittest

from blockchain import Blockchain


class CIATestCase(unittest.TestCase):
    def test_confidentiality(self):
        bc = Blockchain()
        block = bc.add_block("my secret message")
        # ensure ciphertext exists and looks like Fernet token
        self.assertIn('transactions_encrypted', block)
        self.assertTrue(isinstance(block['transactions_encrypted'], str))

    def test_integrity(self):
        bc = Blockchain()
        block = bc.add_block("hello")
        # tamper with ciphertext
        bc.chain[1]['transactions_encrypted'] = 'fake data'
        self.assertFalse(bc.is_chain_valid())

    def test_availability(self):
        bc = Blockchain()
        bc.add_block('test1')
        bc.add_block('test2')
        # corrupt stored hash
        bc.chain[2]['hash'] = '0000deadbeef'
        self.assertFalse(bc.is_chain_valid())


if __name__ == '__main__':
    unittest.main()
