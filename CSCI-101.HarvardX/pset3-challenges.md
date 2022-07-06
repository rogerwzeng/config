### Challenges Encountered in PSET #3
#### Name: Roger Zeng

I created the code in the Python by modeling it after code the professor went through in class. Along the way, I encountered the following challenges:

#### 1. Text field length
I initially underestimated some of the length of the text field by assign values of VARCHAR() length that were too small. I had to subsequently increase the length of the text field to accommodate for them.

In the future, rather than doing it by trial and error, I plan to streamline this process by writing a small Python program to load the csv file into a Pandas dataframe and find the longest length row in each column to guide me in assigning appropriate length of the VARCHAR() text fields..

#### 2. Field values with comma 
During import, some rows (e.g. row 57) would fail and the importation process stopped with an error message. Upon closer examination, I found the error had resulted from some field data containing the field delimiter comma ',', e.g. the "highly_qualified" column in row 57 had a value of "Highly qualified, House Matrix". The comma after the word "qualified" confused the import routine since comma had been specified as the field delimiter (by specifying FIELDS TERMINATED BY ',' ) in the LOAD DATA statement. The part after the comma was assigned to the next column which had caused the error. 

To solve this, I noticed that values of this column had double quote " around them. By adding OPTIONALLY ENCLOSED BY '\\"' in the LOAD DATA statement, I instructed the import routine to treat text enclosed by two double quotes as a single field value, even if it had comma in it! I had to use a backslash \ before the double quote because double quote is a reserved character and had to be escaped by backslash for the interpreter to take it literally.

One interesting note was that the solution suggested by the PSET #3 assignment by adding OPTIONALLY ENCLOSED BY ',' did not work. In fact, it also failed to import the data set because the import routine failed on the same aforementioned row 57. 

#### Conclusion
Other than the above two, I did not encounter other issues with completing this assignment. 
