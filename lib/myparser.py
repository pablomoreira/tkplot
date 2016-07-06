
def sanitize_dir(_text_dir):
	__dir = _text_dir.split(":")
	__sdir =""
	for part in __dir:
		
		if len(part) < 2:
			__sdir += "0" + part
		else:
			__sdir += part #deja un cero delante si es menor que 0xf 
	
	return __sdir

def is_hex_string16(_s):
	hex_digits = set("0123456789abcdef")
	if len(_s) == 16:
		for _char in _s:
			if _char in hex_digits:
				return True
			else:
				return False
	return False
