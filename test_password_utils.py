"""
Unit tests for password_utils module

Tests the pepper, salt, and hash functionality of the password manager.
"""

import unittest
import os
from password_utils import PasswordManager, PasswordPepperError, generate_pepper


class TestPasswordManager(unittest.TestCase):
    """Test cases for PasswordManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_pepper = generate_pepper()
        self.pm = PasswordManager(pepper=self.test_pepper)
        self.test_password = "TestPassword123!"
    
    def test_pepper_initialization_with_parameter(self):
        """Test that PasswordManager initializes with provided pepper"""
        pepper = "a" * 32  # Minimum length pepper
        pm = PasswordManager(pepper=pepper)
        self.assertEqual(pm.pepper, pepper)
    
    def test_pepper_initialization_from_env(self):
        """Test that PasswordManager reads pepper from environment"""
        test_pepper = "b" * 64
        os.environ['PASSWORD_PEPPER'] = test_pepper
        pm = PasswordManager()
        self.assertEqual(pm.pepper, test_pepper)
        del os.environ['PASSWORD_PEPPER']
    
    def test_missing_pepper_raises_error(self):
        """Test that missing pepper raises PasswordPepperError"""
        # Ensure PASSWORD_PEPPER is not set
        if 'PASSWORD_PEPPER' in os.environ:
            del os.environ['PASSWORD_PEPPER']
        
        with self.assertRaises(PasswordPepperError):
            PasswordManager()
    
    def test_short_pepper_raises_error(self):
        """Test that too short pepper raises PasswordPepperError"""
        with self.assertRaises(PasswordPepperError):
            PasswordManager(pepper="tooshort")
    
    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string"""
        password_hash = self.pm.hash_password(self.test_password)
        self.assertIsInstance(password_hash, str)
        self.assertGreater(len(password_hash), 0)
    
    def test_hash_password_contains_argon2id(self):
        """Test that hash contains Argon2id identifier"""
        password_hash = self.pm.hash_password(self.test_password)
        self.assertTrue(password_hash.startswith('$argon2id$'))
    
    def test_empty_password_raises_error(self):
        """Test that empty password raises ValueError"""
        with self.assertRaises(ValueError):
            self.pm.hash_password("")
    
    def test_verify_password_correct(self):
        """Test that correct password verifies successfully"""
        password_hash = self.pm.hash_password(self.test_password)
        self.assertTrue(self.pm.verify_password(self.test_password, password_hash))
    
    def test_verify_password_incorrect(self):
        """Test that incorrect password fails verification"""
        password_hash = self.pm.hash_password(self.test_password)
        self.assertFalse(self.pm.verify_password("WrongPassword", password_hash))
    
    def test_verify_password_empty_inputs(self):
        """Test that empty inputs return False"""
        password_hash = self.pm.hash_password(self.test_password)
        self.assertFalse(self.pm.verify_password("", password_hash))
        self.assertFalse(self.pm.verify_password(self.test_password, ""))
    
    def test_same_password_different_hashes(self):
        """Test that same password produces different hashes (due to salt)"""
        hash1 = self.pm.hash_password(self.test_password)
        hash2 = self.pm.hash_password(self.test_password)
        self.assertNotEqual(hash1, hash2)
        # But both should verify correctly
        self.assertTrue(self.pm.verify_password(self.test_password, hash1))
        self.assertTrue(self.pm.verify_password(self.test_password, hash2))
    
    def test_different_peppers_different_hashes(self):
        """Test that different peppers produce different hashes"""
        pepper1 = "a" * 64
        pepper2 = "b" * 64
        pm1 = PasswordManager(pepper=pepper1)
        pm2 = PasswordManager(pepper=pepper2)
        
        hash1 = pm1.hash_password(self.test_password)
        hash2 = pm2.hash_password(self.test_password)
        
        # Hashes should be different
        self.assertNotEqual(hash1, hash2)
        
        # Each should verify with their own pepper
        self.assertTrue(pm1.verify_password(self.test_password, hash1))
        self.assertTrue(pm2.verify_password(self.test_password, hash2))
        
        # But not with the other pepper
        self.assertFalse(pm1.verify_password(self.test_password, hash2))
        self.assertFalse(pm2.verify_password(self.test_password, hash1))
    
    def test_pepper_is_applied(self):
        """Test that pepper is actually being applied to password"""
        # Create two password managers with different peppers
        pepper1 = "a" * 64
        pepper2 = "b" * 64
        pm1 = PasswordManager(pepper=pepper1)
        pm2 = PasswordManager(pepper=pepper2)
        
        # Hash the same password with both
        hash1 = pm1.hash_password(self.test_password)
        hash2 = pm2.hash_password(self.test_password)
        
        # Verify that hash created with pepper1 doesn't verify with pm2
        self.assertFalse(pm2.verify_password(self.test_password, hash1))
        # And vice versa
        self.assertFalse(pm1.verify_password(self.test_password, hash2))
    
    def test_unicode_password(self):
        """Test that Unicode passwords work correctly"""
        unicode_password = "пароль密码🔐"
        password_hash = self.pm.hash_password(unicode_password)
        self.assertTrue(self.pm.verify_password(unicode_password, password_hash))
        self.assertFalse(self.pm.verify_password("wrongpassword", password_hash))
    
    def test_long_password(self):
        """Test that long passwords work correctly"""
        long_password = "a" * 1000
        password_hash = self.pm.hash_password(long_password)
        self.assertTrue(self.pm.verify_password(long_password, password_hash))
    
    def test_needs_rehash(self):
        """Test needs_rehash functionality"""
        password_hash = self.pm.hash_password(self.test_password)
        # Hash is fresh, should not need rehashing
        self.assertFalse(self.pm.needs_rehash(password_hash))
    
    def test_needs_rehash_invalid_hash(self):
        """Test that invalid hash needs rehashing"""
        self.assertTrue(self.pm.needs_rehash("invalid_hash"))
    
    def test_generate_pepper_length(self):
        """Test that generate_pepper creates correct length"""
        pepper = generate_pepper()
        self.assertEqual(len(pepper), 64)
    
    def test_generate_pepper_uniqueness(self):
        """Test that generate_pepper creates unique values"""
        peppers = [generate_pepper() for _ in range(10)]
        # All should be unique
        self.assertEqual(len(peppers), len(set(peppers)))


class TestPasswordSecurity(unittest.TestCase):
    """Security-focused test cases"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.pepper = generate_pepper()
        self.pm = PasswordManager(pepper=self.pepper)
    
    def test_timing_attack_resistance(self):
        """Test that verification doesn't reveal info through timing"""
        # This is a basic test; real timing attack testing requires more sophisticated methods
        password = "SecurePassword123"
        password_hash = self.pm.hash_password(password)
        
        # Both should return False, ideally in similar time
        self.assertFalse(self.pm.verify_password("", password_hash))
        self.assertFalse(self.pm.verify_password("WrongPassword", password_hash))
    
    def test_hash_not_reversible(self):
        """Test that hash cannot be used to derive password"""
        password = "SecretPassword"
        password_hash = self.pm.hash_password(password)
        
        # Hash should not contain the password
        self.assertNotIn(password, password_hash)
        self.assertNotIn(password.lower(), password_hash.lower())
    
    def test_pepper_not_in_hash(self):
        """Test that pepper is not stored in hash"""
        password = "TestPassword"
        password_hash = self.pm.hash_password(password)
        
        # Pepper should not be visible in hash
        self.assertNotIn(self.pepper, password_hash)


if __name__ == '__main__':
    print("=" * 70)
    print("Running Password Utils Tests")
    print("=" * 70)
    unittest.main(verbosity=2)
