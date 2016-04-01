typedef unsigned long int UINT4; // 32 bit type (4 bytes)

typedef struct {
	UINT4 i[2]; // # bits handled % 2^64
	UINT4 buf[4]; // scratch biffer
	unsigned char in[64]; // input buffer
	unsigned char digest[16]; // actual digest after MD5Final call
} MD5_CTX;

void MD5Init();
void MD5Update();
void MD5Final();