# --- Day 4: Secure Container ---
#
# You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.
#
# However, they do remember a few key facts about the password:
#
#     It is a six-digit number.
#     The value is within the range given in your puzzle input.
#     Two adjacent digits are the same (like 22 in 122345).
#     Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
#
# Other than the range rule, the following are true:
#
#     111111 meets these criteria (double 11, never decreases).
#     223450 does not meet these criteria (decreasing pair of digits 50).
#     123789 does not meet these criteria (no double).
#
# How many different passwords within the range given in your puzzle input meet these criteria?
#
# Your puzzle input is 138241-674034.

def get_digits(n):
	return [int(i) for i in list(str(n))]

def has_adj(n):
	for i in range(5):
		if n[i] == n[i+1]:
			# Beginning:
			if i == 0:
				# something different after
				if n[i+2] != n[i]:
					return True
			# End
			elif (i+2 > 5):
				# something different before
				if n[i] != n[i-1]:
					return True
			else: # Middle
				# something different before and after
				if n[i+2] != n[i] and n[i] != n[i-1]:
					return True
	return False

def increasing(n):
	for i in range(5):
		if n[i] > n[i+1]:
			return False
	return True

def test(n):
	if len(str(n)) != 6:
		#print("out of range")
		return False
	#if n < 138241 or n > 674034:
	#	return False

	digits = get_digits(n)
	#print("Digits: {}".format(digits))
	if not increasing(digits):
		#print("not increasing")
		return False
	if not has_adj(digits):
		#print("no adj")
		return False
	return True

print("test(111111) = {}".format(test(111111)))
print("test(223450) = {}".format(test(223450)))
print("test(123789) = {}".format(test(123789)))

lo = 138241
hi = 674034
num_matches = 0
for i in range(lo, hi+1):
	if test(i):
		num_matches += 1
		print("Found match #{}: {}".format(num_matches, i))
print("Overall, found {} matches".format(num_matches))

