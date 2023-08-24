from django.test import TestCase

# Create your tests here.
cleaned_text = "sssssssssssssssssssssssssssssssssssssssssss"

prompt = f"""
Please generate a summary for the 'Materials and Methods' 
section suitable for a high-standard scientific publication in a renowned 
scientifical journal, based on the protocol provided below. The response 
should closely resemble the level of detail and scientific formality found in 
typical scientific journal the example style:'Mice were killed under anesthesia with 5% chloral hydrate (300 mg/kg), 
which was injected intraperitoneally. The ACC were harvested on ice and lysed 
in ice-cold radioimmunoprecipitation assay (RIPA) lysis buffer 
(Applygen Technologies Inc., Beijing, China), which contains protease inhibitors.'
In response use past time in the sentences. The response should be structured in 
the following sections: 'Protocol Description:' (maximum 50 words), 
'Title:' (suggested protocol title), and 
'Methods:' (the primary content of the materials and methods section, 
try to use maximum 150 words in this section). Ensure you focus on key details 
and present them in a formal scientific language.
[Protocol: {cleaned_text}]
Ensure the 'Methods' section includes specifics about the materials used, procedures, 
equipment, software, and any other vital details. Ensure that the sections are propertly named 
as ;Title:', 'Description:' and 'Methods:' and all of them contain the content.
"""

print(prompt)