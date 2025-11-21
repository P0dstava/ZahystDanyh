using System;
using System.Security.Cryptography;
using CryptoExamples;

class Program
{
    static void Main()
    {
        // Генеруємо ключ та nonce
        byte[] key = new byte[32]; // AES-256
        byte[] nonce = new byte[8]; // тут ми використовуємо 8-байтний nonce
        using (var rng = RandomNumberGenerator.Create())
        {
            rng.GetBytes(key);
            rng.GetBytes(nonce);
        }

        string message = "Hello, AES-CTR! Це тестове повідомлення.";
        Console.WriteLine("Original: " + message);

        var cipher = AesCtr.Encrypt(key, nonce, System.Text.Encoding.UTF8.GetBytes(message));
        Console.WriteLine("Cipher (Base64): " + Convert.ToBase64String(cipher));

        var decrypted = AesCtr.Decrypt(key, nonce, cipher);
        string plain = System.Text.Encoding.UTF8.GetString(decrypted);
        Console.WriteLine("Decrypted: " + plain);

        Console.WriteLine("Equal: " + (message == plain));
    }
}
