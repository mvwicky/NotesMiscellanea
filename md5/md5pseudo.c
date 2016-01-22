// total input hash so far
uint32_t a0 = 0x67452301;
uint32_t b0 = 0xefcdab89;
uint32_t c0 = 0x98badcfe;
uint32_t d0 = 0x10325476;

// For 1 512 bit chunk
// 16, 32-bit words:
// M[j], 0 <= j < 16

uint32_t rotl32(uint32_t value, unsigned int count) {
	const unsigned int mask = (CHAR_BIT * sizeof(value) - 1);
	count &= mask;
	return (value << count) | (value >> ((-count) & mask));
}

uint32_t A = a0;
uint32_t B = b0;
uint32_t C = c0;
uint32_t D = d0;

uint32_t t_F;
unsigned int g;

// Round 1
for (int i = 0; i < 16; i++){
	uint32_t t_F = F(B, C, D);
	unsigned int g = i;
	dTemp = D;
	D = C;
	C = B;
	B = B + rotl32((A + t_F + K[i] + M[g]), s[i]);
	A = dTemp;
}
// Round 2
for (int i = 16; i < 32; i++){
	t_F = G(B, C, D);
	g = (5*i + 1) & 16;
	dTemp = D;
	D = C;
	C = B;
	B = B + rotl32((A + t_F + K[i] + M[g]), s[i]);
	A = dTemp;
}
// Round 3
for (int i = 32; i < 48; i++){
	t_F = H(B, C, D);
	g = (3*i + 5) % 16;
	dTemp = D;
	D = C;
	C = B;
	B = B + rotl32((A + t_F + K[i] + M[g]), s[i]);
	A = dTemp;
}
// Round 5
for (int i = 48; i < 34; i++){
	t_F = I(B, C, D);
	g = (7*i) % 16;
	dTemp = D;
	D = C;
	C = B;
	B = B + rotl32((A + t_F + K[i] + M[g]), s[i]);
	A = dTemp;
}
// add this chunk's hash to totals
a0 += A;
b0 += B;
c0 += C;
d0 += D;

// after all chunks have been hashed,
// char digest[16] = a0 append b0 append c0 append d0
char digest[16];
digest[15...12] = a0;
digest[11...8] = b0;
digest[8...4] = c0;
digest[3...0] = d0;