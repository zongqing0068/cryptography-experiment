#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>
#include <openssl/sha.h>

unsigned char *additionalMsg = "&download=secret.txt";

// The MAC for the valid URL
int a[8] = {  0x77b18d72, 0xd2db6e52, 0x98f70402, 0x27b8ba8e,
              0x376a667e, 0xfebbfa95, 0x2fb5837d, 0x12c7319c };



int main(int argc, const char *argv[])
{
  int i;
  unsigned char buffer[SHA256_DIGEST_LENGTH];
  SHA256_CTX c;

  SHA256_Init(&c);

  /* We assume that the padded original message has 64 bytes (i.e., 1 block).
   * If that is not true, modify 64 accordingly, e.g. use 128 for 2 blocks. 
   * This step is important, because that is how we tell the hash function
   * the length of our message. */
  for (i=0; i<64; i++)  SHA256_Update(&c, "*", 1);

  for (i=0; i<8; i++)   c.h[i] = htole32(a[i]);

  // Append the additional message
  SHA256_Update(&c, additionalMsg, strlen(additionalMsg));
  SHA256_Final(buffer, &c);
  for (i = 0; i < 32; i++) {
      printf("%02x", buffer[i]);
  }
  printf("\n");

  return 0;
}
