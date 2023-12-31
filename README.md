# Paper title creator
Tool to create a paper title based on year, name and content of paper PDF.

Tool reads in PDFs of academic papers, parses the text, uses OpenAI's API to extract the year of publication, first author name, and subject of the paper, and renames the papers in the format `{year}_{name}_{description}.pdf`.
A single paper can be read in by specifiying the input_path and input_file_name arguments, or a directory of papers can be read in by specifying just the input_path argument.

### Example usage
For a directory of papers:  
`python main.py --input_path='papers/' --input_file_name='2309.12288.pdf' --api_key_path="../../openai_key.txt" --output_path="output/"`  
For a directory of papers:  
`python main.py --input_path='papers/' --api_key_path="../../openai_key.txt" --output_path="output/"`

### TODOs:
- [ ] More secure way of reading in API key
- [ ] Using NLP package like NLTK/spaCy to offer offline way of parsing papers
- [ ] Additional command line arguments:
  - [ ] OpenAI/NLTK mode
  - [ ] Model option (e.g. 'gpt-3.5-turbo')
- [ ] OpenAI credits cost estimate
- [ ] Move main function to its own function so can be imported and used in notebooks
- [ ] Make sure population of duplicate files is avoided:
	- [ ] Check if that file has already been copied to the output directory
	- [ ] What happens if there are papers that share names and years? and topics?
	- [ ] Maybe have a letter after the name, so 2023_Li_b_hallucinations.pdf?
	- [ ] Maybe a command line argument to copy or create differently named files?
- [ ] Units tests
- [ ] Think of more edge cases for file names, text parsing etc.
- [ ]Some way of benchmarking the performance of different methods, e.g. how many years and names of ~20 papers were extracted correctly?
