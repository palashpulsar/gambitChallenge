def longConversion(regA, regB):
	bin_form = format(regB, '016b') + format(regA, '016b')
	print bin_form
	if bin_form[0] == '1':
		# Number is negative
		bin_form_Compliment = twoCompliment(bin_form)
		return -int(bin_form_Compliment, 2)
	else:
		return int(bin_form, 2) 

def twoCompliment(bin_form):
	result = [0]*len(bin_form)
	carryBit = 1
	for i in range(len(bin_form)):
		if bin_form[i] == '0':
			result[i] = '1'
		else:
			result[i] = '0'
	print "one's complement: %s" %result 

	# Adding 1 at the end
	if result[-1] == '0':
		result[-1] = '1'
	else:
		resultLength = len(result)
		for i in range(resultLength):
			if carryBit == 0:
				break
			if result[resultLength-i-1] == '1':
				result[resultLength-i-1] = '0'
				carryBit = 1
			else:
				result[resultLength-i-1] = '1'
				carryBit = 0
	print "two's complement: %s" %result 
	print type(result)
	return ''.join(result)

regA = 65480
regB = 65535
result = longConversion(regA, regB)
print result

# def real4Conversion(regA, regB):
# 	"""
# 	Description:
# 	This function converts REAL4 formatted data to human readable.

# 	Input:
# 	regA and regB: The two register values for a particular variable.

# 	Output:
# 	value: The human readable equivalent of the binary(regB)+binary(regA)
# 	"""
# 	bin_form = format(regB, '016b') + format(regA, '016b')
# 	bin_form = bin_form[::-1]
# 	sign_value = 0.0
# 	exponent_value = 0.0
# 	fraction_value = 1.0

# 	for i in range(len(bin_form)):
# 		if i < 23:
# 			if int(bin_form[i]) == 1:
# 				fraction_value += int(bin_form[i]) *2**(i-23)
# 		elif i >= 23 and i <= 30:
# 			exponent_value += int(bin_form[i]) *2**(i-23)
# 		else:
# 			sign_value = (-1)**int(bin_form[i])

# 	value = sign_value * fraction_value * 2**(exponent_value-127)
# 	return value


# regA = 15568 # 57130 # 
# regB = 16611 # 17566 # 
# print real4Conversion(regA, regB)

