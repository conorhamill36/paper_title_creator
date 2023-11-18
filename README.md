# paper_title_creator
Tool to create a paper title based on year, name and content of paper PDF.

Tool reads in PDFs of academic papers, parses the text, uses OpenAI's API to extract the year of publication, first author name, and subject of the paper, and renames the papers in the format '{year}_{name}_{description}.pdf'.
A single paper can be read in by specifiying the input_path and input_file_name arguments, or a directory of papers can be read in by specifying just the input_path argument.

### Example usage
For a directory of papers: python main.py --input_path='papers/' --input_file_name='2309.12288.pdf' --api_key_path="../../openai_key.txt" --output_path="output/"
For a directory of papers: python main.py --input_path='papers/' --api_key_path="../../openai_key.txt" --output_path="output/"

### TODOs:
- More secure way of reading in API key
- Using NLP package like NLTK to offer offline way of parsing papers
- Additional command line arguments:
  - OpenAI/NLTK mode
  - Model option (e.g. 'gpt-3.5-turbo')
- OpenAI credits cost estimate 
