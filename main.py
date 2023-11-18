# Main file for running get paper title
import shutil, os

from PyPDF2 import PdfReader
from openai import OpenAI


def get_api_key(api_key_path):
    """
    Gets api key from filepath
    """
    with open(api_key_path) as f:
        api_key = f.readline().strip()
    return api_key


def extract_text_from_pdf(dir_path, file_name):
    """
    Uses reader object to read in first page of pdf in dir_path, under assumption all important will be on the first page
    """
    reader = PdfReader(dir_path + file_name)
    page = reader.pages[0]
    return page.extract_text()


def openai_api_call(client, message, model='gpt-3.5-turbo'):
    """
    Makes call to openai API and returns text of response
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": message},
        ]
    )
    return response.choices[0].message.content


def get_new_filename(client, message, model='gpt-3.5-turbo', file_extension='.pdf'):
    """
    Returns new file name, using openai to generate a name
    """
    api_response = openai_api_call(client=client, message=message, model=model)
    # validate filename
    
    # unpacking filename
    year, name, *descriptions = api_response.split("_")
    assert year.isnumeric() # check year is a number
    assert int(year) > 1800 # check year is a sensible number
    assert name.isalpha() # check name has no numbers

    name = name.title() # capitalise name
    descriptions = [description.lower() for description in descriptions] # making all description strings lowercase
    
    new_filename = '_'.join([year, name, *descriptions]) + ".pdf" # joining filename components and adding file extension
    
    return new_filename


PROMPT_CONTEXT = """
    You are a helpful assistant who helps name the files for academic papers.
    The following is text extracted from the first page of an academic paper.
    Return a single slug containing the year, surname of the author and two/three words describing the paper subject, separated by underscores.

"""


if __name__ == "__main__":
    print("Hello world!")

    # variables
    api_key_path = "../../openai_key.txt"
    input_path = "data/"
    input_file_name = "2311.01901.pdf"
    # input_file_name = None
    output_path = "output/"

    if input_file_name is None:
        print(f"processing all .pdf files in {input_path}:")
        # get all pdfs from dir
        input_file_names = list(filter(lambda x: x.endswith('.pdf'), os.listdir(input_path)))
    else:
        # if input filename is specified, only reading in that single file
        input_file_names = [input_file_name]

    # looping over all file names
    for input_file_name in input_file_names:
        # Extract text from PDF
        text = extract_text_from_pdf(dir_path=input_path, file_name=input_file_name)

        # get api key
        api_key = get_api_key(api_key_path=api_key_path)
        
        # send text to OpenAI API
        client = OpenAI(api_key=api_key)
        prompt = PROMPT_CONTEXT + text
        print(f"Making OpenAI API call for file {input_file_name}...")
        new_filename = get_new_filename(client=client, message=prompt)
        print("OpenAI API call finished.")

        # copy pdf to new directory under new name
        shutil.copy(
            src=input_path + input_file_name,
            dst=output_path+new_filename, 
        )

        # assert that file under new name is in the new filepath
        assert new_filename in os.listdir(output_path)
        print(f"{input_path}{input_file_name} has been named {new_filename} and copied to {output_path}")
