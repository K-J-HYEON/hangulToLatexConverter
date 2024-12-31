import hml_equation_parser as hp
import codecs

doc = hp.parseHmlSample("sample.hml")  # parse hml document and make ElementTree

doc = hp.convertEquationSample(doc)  # find equations from ElementTree and convert them to latex string
string = hp.extract2HtmlStrSample(doc)  # convert ElementTree to html document with MathJax.

f = codecs.open("sample.hml", "w", "utf8")
f.write(string)
f.close()