using System;
using System.Security.Cryptography;
using Xunit;
using AesCtrProject;

namespace AesCtrTests
{
    public class EncryptionTests
    {
        [Fact]
        public void Encrypt_Then_Decrypt_ReturnsOriginal()
        {
            byte[] key = new byte[32];
            byte[] nonce = new byte[8];

            using (var rng = RandomNumberGenerator.Create())
            {
                rng.GetBytes(key);
                rng.GetBytes(nonce);
            }

            string original = "Unit test AES CTR example";

            var encrypted = AesCtr.Encrypt(key, nonce, System.Text.Encoding.UTF8.GetBytes(original));
            var decrypted = AesCtr.Decrypt(key, nonce, encrypted);

            string result = System.Text.Encoding.UTF8.GetString(decrypted);

            Assert.Equal(original, result);
        }

        [Fact]
        public void DifferentNonce_ProducesDifferentCiphertext()
        {
            byte[] key = new byte[32];
            byte[] nonce1 = new byte[8];
            byte[] nonce2 = new byte[8];

            using (var rng = RandomNumberGenerator.Create())
            {
                rng.GetBytes(key);
                rng.GetBytes(nonce1);
                rng.GetBytes(nonce2);
            }

            string message = "Same message";

            var c1 = AesCtr.Encrypt(key, nonce1, System.Text.Encoding.UTF8.GetBytes(message));
            var c2 = AesCtr.Encrypt(key, nonce2, System.Text.Encoding.UTF8.GetBytes(message));

            Assert.NotEqual(Convert.ToBase64String(c1), Convert.ToBase64String(c2));
        }
    }
}
