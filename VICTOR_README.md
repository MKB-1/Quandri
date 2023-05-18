## Architecture
For the task of retrieving data from Wikipedia and outputting a new file created from that data, I chose to separate the robot logic into two parts.
First, a producer robot which creates work items, in this case, work items are json files with the necessary data.
Second, a consumer robot which consumes work items, in this case, it performs some minimal calculations on the data and generates a single markdown file to contain all the information from the multiple json files.
I also had a shared package which contains functionality shared by both robots, as well as custom typings to describe the data.
This is the architecture suggested by <a href="https://robocorp.com/docs/courses/work-data-management/break-your-robot-into-multiple-files">Robocorp</a>, because it allows parallelization of tasks in the cloud.

## Error Handling
Both the producer and consumer robots do not crash when encountering most errors you would expect to see from this task.
For a given search term (i.e. scientist names), the errors from the *producer* are when it goes to a webpage with a different format than expected. If it cannot find the first paragraph and the infobox elements, the search term is skipped.
When extracting birth date and death date, if that data is not available on the infobox, the extracted_birth_date and extracted_death_date keys are not created in the json file.

For a given file name, the errors from the *consumer* are when the file does not exist and when extracted_birth_date and extracted_death_date keys cannot be found in the json file. When either of these errors are encountered, the data from the file is not appended to the markdown file.

I have edited the SCIENTIST list to include a term which yields each type of error. Therefore, for both these producer and consumer, the handling of the error can be observed by simply running the robots.

## Logging
In addition to the stdout.log file which is automatically generated, I included an extra log file for each robot, located in the output directory (e.g. producer/output).