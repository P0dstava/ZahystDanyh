using System;
using System.IO;
using System.Linq;
using System.Security.Cryptography;

namespace CryptoExamples
{
    public static class AesCtr
    {
        // Генерує AES-CTR keystream блоки використовуючи AES-ECB (без паддінгу).
        // key: 16/24/32 байт (AES-128/192/256)
        // nonce: довжина максимум 15 байт (залишає 1..8 байт для counter) — тут ми використаємо 8 байт nonce + 8 байт counter (можна змінити)
        // plaintext: байти для шифрування (допускається будь-яка довжина)
        public static byte[] Encrypt(byte[] key, byte[] nonce, byte[] plaintext)
        {
            if (key == null) throw new ArgumentNullException(nameof(key));
            if (nonce == null) throw new ArgumentNullException(nameof(nonce));
            if (plaintext == null) throw new ArgumentNullException(nameof(plaintext));
            if (nonce.Length != 8) throw new ArgumentException("Цей приклад очікує nonce довжини 8 байт.", nameof(nonce));

            return ProcessCtr(key, nonce, plaintext);
        }

        // CTR шифрування і дешифрування однакові
        public static byte[] Decrypt(byte[] key, byte[] nonce, byte[] ciphertext)
        {
            return Encrypt(key, nonce, ciphertext);
        }

        private static byte[] ProcessCtr(byte[] key, byte[] nonce, byte[] input)
        {
            const int blockSize = 16;
            var output = new byte[input.Length];

            using (Aes aes = Aes.Create())
            {
                aes.Mode = CipherMode.ECB;
                aes.Padding = PaddingMode.None;
                aes.Key = key;

                using (ICryptoTransform encryptor = aes.CreateEncryptor())
                {
                    // блоков keystream
                    long blockCount = (input.Length + blockSize - 1) / blockSize;
                    // використовуємо 8 байт nonce + 8 байт лічильника (big-endian)
                    for (long i = 0; i < blockCount; i++)
                    {
                        byte[] counterBlock = new byte[blockSize];
                        // nonce (8 байт) у початок
                        Buffer.BlockCopy(nonce, 0, counterBlock, 0, nonce.Length);
                        // counter (8 байт) big-endian
                        byte[] counterBytes = BitConverter.GetBytes((ulong)i);
                        if (BitConverter.IsLittleEndian)
                            Array.Reverse(counterBytes);
                        Buffer.BlockCopy(counterBytes, 0, counterBlock, nonce.Length, Math.Min(counterBytes.Length, blockSize - nonce.Length));

                        byte[] keystreamBlock = new byte[blockSize];
                        encryptor.TransformBlock(counterBlock, 0, blockSize, keystreamBlock, 0);

                        int offset = (int)(i * blockSize);
                        int remaining = Math.Min(blockSize, input.Length - offset);
                        for (int j = 0; j < remaining; j++)
                        {
                            output[offset + j] = (byte)(input[offset + j] ^ keystreamBlock[j]);
                        }
                    }
                }
            }

            return output;
        }

        // Допоміжні методи для зручності (Base64 представлення)
        public static string EncryptToBase64(string keyBase64, string nonceBase64, string plaintextUtf8)
        {
            var key = Convert.FromBase64String(keyBase64);
            var nonce = Convert.FromBase64String(nonceBase64);
            var plain = System.Text.Encoding.UTF8.GetBytes(plaintextUtf8);
            var cipher = Encrypt(key, nonce, plain);
            return Convert.ToBase64String(cipher);
        }

        public static string DecryptFromBase64(string keyBase64, string nonceBase64, string cipherBase64)
        {
            var key = Convert.FromBase64String(keyBase64);
            var nonce = Convert.FromBase64String(nonceBase64);
            var cipher = Convert.FromBase64String(cipherBase64);
            var plain = Decrypt(key, nonce, cipher);
            return System.Text.Encoding.UTF8.GetString(plain);
        }
    }
}
