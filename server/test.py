strs="""{

"sign":{"user":"5bdeaa3806c65427eeda2499",
"text":"PowerBank Scan in ["E28N50", "E29N50", "E30N50", "E31N50", "E32N50", "E30N51", "E30N52"]",
"time":12618855
}
}

"""
import json5

js=json5.loads(strs,parse_constant=lambda x:print(type(x),x))
print(js)