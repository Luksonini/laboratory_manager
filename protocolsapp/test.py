import openai
import os
from docx import Document
import re

os.environ['OPEN_API_KEY'] = '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'
openai.api_key = os.getenv('OPEN_API_KEY')

def remove_empty_lines(file_name):
    base_path = r"D:\programowanie\Lab_Manager3\event-calendar\uploads"
    full_path = os.path.join(base_path, file_name)
    doc = Document(full_path)
    # Usuń puste wiersze i złącz wszystkie paragrafy w jeden string
    cleaned_text = ' '.join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip() != ''])
    
    return cleaned_text

def create_protocol_prompt(file_name):
    prompt = f"""
    "Please generate a summary for the 'Materials and Methods' 
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
    [Protocol: {remove_empty_lines(file_name)}]
    Ensure the 'Methods' section includes specifics about the materials used, procedures, 
    equipment, software, and any other vital details. Ensure that the sections are propertly named 
    as ;Title:',  'Description:' and 'Methods:' and all of them contain the content.
    """
    return prompt

prompt = create_protocol_prompt("Protokół-TAPS-NEBNext.docx")
response = openai.ChatCompletion.create(
        model="gpt-4",
        max_tokens=1024,
        n=1,
        stop=None,
        messages=[{'role':'user', "content": prompt}],
        temperature=0.7,
    )  


response = openai.ChatCompletion.create(model="gpt-4", max_tokens = 1024, temperature=0.5, n=1, messages=[{'role':'system', "content": prompt}])
result = response['choices'][0]["message"]["content"]

# Wyciągnięcie tytułu
title_match = re.search(r"Title: (.*?)\s*Protocol Description:", result)
title = title_match.group(1) if title_match else None

# Wyciągnięcie opisu protokołu
description_match = re.search(r"Protocol Description: (.*?)\s*Methods:", result)
description = description_match.group(1) if description_match else None

# Wyciągnięcie metody
methods_match = re.search(r"Methods: (.*)", result, re.DOTALL)  # re.DOTALL sprawia, że . obejmuje również znaki nowego wiersza
methods = methods_match.group(1) if methods_match else None

print("Title:", title)
print("Description:", description)
print("Methods:", methods)

