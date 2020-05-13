import rstr

def generate(regex):
    val=""
    # Generate random strings until we find one the right length
    val = rstr.xeger(regex)

    return val