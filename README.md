# anonymize
This is a general purpose data anonymizer. Whilst there are loads of other open source projects which offer the ability to generate anonymized data; to identify data which might need to be anonymized; or to use ML to identify Personally Identifiable Information (PII) - none seemed to meet the requirements I've had on so many occasions. When testing either integration code or testing a data migration I find the need to perform anonymization which meets the following criteria
* Maintain the values in certain fields unchanged (e.g. non-PII fields)
* Replace the values of some fields with 'realistic garbage'. Meaning this should be similar to the original data. In this case it's important to provide data which includes a realistic set of  
  * sizes: if the real data contains values ranging from 3 to 300 characters long, always generating something 10 characters long isn't realistic (code which couldn't deal with long strings would not be tested), but neither would setting all fields to the longest value (this would make the data set unrealistically large).
  * range of values: For instance does the real data include only A-Z or other Latin alphabet characters (such as apostrophes in surnames like O'Flynn), or non-Latin alphabet characters (such as Arabic or Chinese characters) 
  * the pattern which fields follow - in some cases this may not be important but in others it may be important to generate values which meet a certain format (e.g. UK phone numbers must begin with a + or a 0, however no other character other than the first should be a +)
* Replace values with a Token (**consistent** realistic garbage) - random garbage is ok in some cases, but when anonymizing lots of files it may be important to perform anonymisation consistently across multiple records either in the same file or in different files. For instance an invoice number needs to be anonymized not just on the invoice record but also on each invoice line. Generating different anonymous data for each record would break the relationship
* Avoid reversability - ensure that a field cannot be reverse engineered to find the original, or brute forced (so no hashing on values)
* Allow deanonymization - it may be necessary for those who have access to the anonymized data to raise a query about a particular record with whoever did the anonymization. Therefore such the anonymizer should be able to map an anonymized field back to the original for troubleshooting purposes.

To meet these requirements this project includes two tools:
1. Anonymizer: Processes one or many source files and based on a set of rule (in a config file) anonymizes each field to produce one or many output files
2. Analyser: Analyses a source file and produces a rules file to define the structure and what is 'realistic' (e.g. what range of sizes or what patterns do each field follow). This rules file can be further  modified manually before running the anonymizer - alternatively rules files can be written manually and the analyser avoided completely.

# Getting started
## Installation
`pip install -r requirements.txt`

## Running the anonymizer
```mermaid
graph LR
  s[Source Files] --> A(Anonymizer)
  C[Config File] --> A
  A --> O[Output Files]
```
The anonymizer is run from the command line with the following parameters
- -type: The name of the type of file (e.g. customers)
- -rules: (optional) The name of the rules file (defaults to the name of the type with a .cf extension e.g. customers.cf)
- -output: (optional) The folder to put the resulting files (defaults to ./output/)
- -verbose: (optional) Runs in verbose mode outputting more details during the execution
- files: a list of files or wildcard to denote the files to be anonymized - output files have the same name but in the output folder

## Running the analyser
The analyser is similarly run from the command line with the following parameters
- -type The name of the type of file (e.g. customers)
- -delimiter (optional but either delimiter/widths is required) specifies the delimiter used to separate each field in a delimiter separated file (e.g. a comma in a CSV)
- -widths (optional but either delimiter/widths is required) a comma separated list of the widths of each field in a fixed width file (e.g. 1,5,1,2 if the file structure looks like A00000B11)
- -rules (optional) specifies the name of the rules file to create (defaults to the name of the type with a .cf extension e.g. customers.cf)
- -verbose: (optional) Runs in verbose mode outputting more details during the execution
- files a list of files or a wildcard to denote the files to be analysed

# Configuration
Each rules file contains a header with the following:
* Type - the type of file as specified by the -type parameter
* Header (optional) does the first line of the file denote a header (default to false)
* Delimiter (optional - if not present this denotes fixed width)

The rules configuration file contains a field list with the following values for each field
* Field name: The unique name for each field. If the rules file was generated by the analyser this will be in the form TYPE_field_COUNT with count starting a 1 (e.g. customers_field_1). It's important to rename this if tokenised fields need to be used consistently across file types (e.g. if the accounts and customers files both need a customer ID field then the fieldname in both configuration files must share the same field name)
* Mode: The method of anonymisation applied to this field. This can be:
  * *random* - generate a random value meeting the rules specified below
  * *token* - replace with a token which meets the rules specified below (the first time this value is found a random token will be gemerated, but subsequent values will recieve the same token)
  * *original* - keep the original value unchanged  
* Width (only for fixed width files): The size of this field in characters
* RegEx: The regular expression which must be satisfied when generating a field
* PresentRatio: The probability of this field being non-empty (all spaces for fixed length or zero length for delimted files) - e.g. 0 means never present, 1 means always contains data, 0.5 means contains data half the time

# Tokenisation
Token values are stored in files in the ./mapping folder. There is one file per tokenised field. The file contains:
* Field name (as defined in the Configuration file)
* original value
* anonymized value

**Note: These files contain _original_ values and are stored unencrypted so these MUST be handled with the same care as the source files and deleted when no longer needed.**