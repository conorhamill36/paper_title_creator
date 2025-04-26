# Main file for running get paper title
import argparse
import os
import shutil

import openai
from openai import OpenAI

from helpers.llm_helpers import openai_api_call, get_api_key, PROMPT_CONTEXT
from helpers.text_helpers import extract_text_from_pdf


def get_new_filename(
    client: openai.Client,
    message: str,
    model: str = "gpt-3.5-turbo",
    file_extension=".pdf",
):
    """
    Returns new file name, using openai to generate a name
    """
    api_response = openai_api_call(client=client, message=message, model=model)
    # validate filename

    # unpacking filename
    year, name, *descriptions = api_response.split("_")
    assert year.isnumeric()  # check year is a number
    assert int(year) > 1800  # check year is a sensible number
    assert name.isalpha()  # check name has no numbers

    name = name.title()  # capitalise name
    descriptions = [
        description.lower() for description in descriptions
    ]  # making all description strings lowercase

    new_filename = (
        "_".join([year, name, *descriptions]) + ".pdf"
    )  # joining filename components and adding file extension

    return new_filename


def get_paper_file_name(
    input_path: str, input_file_name: str, api_key_path: str
) -> str:
    """Gets the string to rename the file"""
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

    return new_filename


def create_paper_files(
    input_path: str, output_path: str, api_key_path: str, input_file_name: str = None
):
    if input_file_name is None:
        print(f"processing all .pdf files in {input_path}:")
        # get all pdfs from dir
        input_file_names = list(
            filter(lambda x: x.endswith(".pdf"), os.listdir(input_path))
        )
    else:
        # if input filename is specified, only reading in that single file
        input_file_names = [input_file_name]

    # looping over all file names
    for input_file_name in input_file_names:

        # Get new filename
        new_filename = get_paper_file_name(
            input_path=input_path,
            input_file_name=input_file_name,
            api_key_path=api_key_path,
        )

        # copy pdf to new directory under new name
        shutil.copy(
            src=input_path + input_file_name,
            dst=output_path + new_filename,
        )
        print(
            f"{input_path}{input_file_name} has been named {new_filename} and copied to {output_path}"
        )

        # assert that file under new name is in the new filepath
        assert new_filename in os.listdir(output_path)


if __name__ == "__main__":

    # Parsing command line arguments
    parser = argparse.ArgumentParser(
        description="Process some arguments.", argument_default=None
    )
    parser.add_argument("--input_path", required=False, default=".")
    parser.add_argument("--input_file_name", required=False, default=None)
    parser.add_argument("--output_path", required=False, default=".")
    parser.add_argument("--api_key_path", required=True)

    args = parser.parse_args()
    input_path = args.input_path
    input_file_name = args.input_file_name
    output_path = args.output_path
    api_key_path = args.api_key_path

    create_paper_files(
        input_path=input_path,
        input_file_name=input_file_name,
        output_path=output_path,
        api_key_path=api_key_path,
    )
