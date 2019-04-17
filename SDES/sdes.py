#Small code, huge explaination :P
# Simplified DES

# Three Phases: Key Generation, Encryption, Decryption

# KEY GENERATION
## SDES goes through 2 rounds so we need 2 keys
## 10 bit key
## Pass through P10 permutation
## Divide key into two halves
## Pass both halves through Left Shift by 1
## Join and pass through P8 permutation
## and... we have KEY1

### Chosen randomly
key ="1010000010"
P10 =(3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8 = (6, 3, 7, 4, 8, 5, 10, 9)

### Permutation function
def permutation(perm_seq,key):
	new_key = ""
	for i in perm_seq:
		new_key += key[i-1]
	return new_key

### Key 1
def key1(key):
	p10_key = permutation(P10,key)
	print "After P10: ",p10_key
	key_half1 = p10_key[:5]
	print "First half: ",key_half1
	key_half2 = p10_key[5:]
	print "Second half: ",key_half2
	left_shift1 = key_half1[1:]+key_half1[:1]
	print "Left shift first half: ",left_shift1
	left_shift2 = key_half2[1:]+key_half2[:1]
	print "Left shift second half: ",left_shift2
	p8_key = permutation(P8,str(left_shift1+left_shift2))
	print "Key after P8 permutation",p8_key
	return p8_key,left_shift1,left_shift2

k1,left_shift1,left_shift2 = key1(key)
print "First key is: ",k1

## Use the Left Shifted half keys
## Left shift it again by 2 
## Join and pass through P8
## we have KEY2!
def key2(left_shift1,left_shift2):
	left_shift1_by2 = left_shift1[2:]+left_shift1[:2]
	print "Left shift previous left shift by 2: ",left_shift1_by2
	left_shift2_by2 = left_shift2[2:]+left_shift2[:2]
	print "Left shift second half by 2: ",left_shift2_by2
	p8_key2 = permutation(P8,str(left_shift1_by2+left_shift2_by2))
	return p8_key2

k2 = key2(left_shift1,left_shift2)
print "Second key is: ",k2


# Phase 2 : ENCRYPTION

## You take your 8 bit plaintext
## Pass it through initial permutation(IP) sequence

## Divide it into two halves
## Leave the first half as is
## Take the second half and expand it through expansion permutation(EP) 
## XOR this with KEY1
## Divide that into two parts and pass through Sboxes : s1,s2 resulting in 2 bits each
## Combine these and pass 4 bits through P4 permutation
## XOR this with the first half left as is
## this gives new first half and second half

## for the second round we swap these two
## go through all the steps that come after IP again

### Plaintext
plaintext = "01110010"
print "Given plaintext: ",plaintext
### Initial Permutation
IP = (2, 6, 3, 1, 4, 8, 5, 7)
new_plaintext = permutation(IP,plaintext)
print "Plaintext after IP: ",new_plaintext
### Divide into two
pt_1 = new_plaintext[:4]
print "Plaintext part 1: ",pt_1
pt_2 = new_plaintext[4:]
print "Plaintext part 2: ",pt_2

### Two rounds with different keys so a common round function


EP = (4, 1, 2, 3, 2, 3, 4, 1)

S0 = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
     ]

S1 = [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]
     ]

P4 = (2, 4, 3, 1)

def Round(pt_1,pt_2,key):
	part2_expansion = permutation(EP,pt_2)
	print "Expansion of plaintext part 2: ",part2_expansion
	xor_key = bin(int(key,2)^int(part2_expansion,2))[2:].zfill(8)
	print "After Xor with key: ",xor_key
	# divide it into half and pass it through sboxes
	xor_key1 = xor_key[:4]
	print "First half: ",xor_key1
	xor_key2 = xor_key[4:]
	sbox1 = sbox(S0,xor_key1)
	print "First half through S0: ",sbox1
	sbox2 = sbox(S1,xor_key2)
	print "Second half through S1: ",sbox2
	combined_sbox = sbox1+sbox2
	print "Combined Sbox: ",combined_sbox
	p4_text = permutation(P4,combined_sbox)
	xored_p4 = bin(int(pt_1,2)^int(p4_text,2))[2:].zfill(4)
	return xored_p4,pt_2

# The sbox function
def sbox(sbox_name,text):
	# In the sbox we have a matrix with numbers
	# Row is chosen using text digits 1 and 4
	row = int(text[0]+text[3],2)
	#print row
	# Column is chosen using 2 and 3
	column = int(text[1]+text[2],2)
	#print column
	# we want the binary version of the number at that location in the sbox
	#print sbox_name[row][column]
	return bin(sbox_name[row][column])[2:].zfill(2)	
	



round1_part1,round1_part2 = Round(pt_1,pt_2,k1)
print "Round 1 part 1 & 2: ",round1_part1,round1_part2

#swap the outputs from round 1 and give it to round 2

round2_part1,round2_part2 = Round(round1_part1,round1_part2,k2)
print "Round 2 part 1 & 2: ",round2_part1,round2_part2

# Pass the round 2 results through IP inverse permutation

IPi  = (4, 1, 3, 5, 7, 2, 8, 6)

#Cipher text finally

cipher = permutation(IPi,round2_part1+round2_part2)

print "Cipher Text: ",cipher

# Phase 3: DECRYPTION

## Pass cipher text through rounds after IP
## first k2 then k1
## then inverse IP again

decrypt1 = permutation(IP,cipher)
decrypt2_1,decrypt2_2 = Round(decrypt1[:4],decrypt1[4:],k2)
decrypt3_1,decrypt3_2 = Round(decrypt2_1,decrypt2_2,k1)
plaintext_again = permutation(IPi,decrypt3_1+decrypt3_2)
print "Plaintext Again: ",plaintext_again

