# gluco-plot
Is a web app (python with Flask Frame work) which uploads the gluco-meter reading in CSV and plots

* Line Chart
* Pie Chart
* Box Plot
* Gauge Chart

of your data. You can also save the plot as file.

###### Installing

Install the dependencies for the application
> pip install -r requirements.txt

#### Customizing your CSV file type.

1. The file _format.json_  contains the CSV format of the file. Add your own file format to this file if you need.  
   Shown below is for [mySugr](https://mysugr.com/logbook/) CSV file format.  
   The `date` is at _column 0_ , `time` is at _column 1_ and `mgdl` is at _column 3_.   
  The `datefmt` is the date format of your CSV file expressed in UNIX date time structure,   
   The  `lines_to_skip` is the number of lines / rows to skip the header.

    ~~~yaml
    {
        "mysgr":{
            "comment_csvcol":"The columns in CSV to get the information we need",
            "csvcol":{
                "date":0,
                "time":1,
                "mgdl":3
            },
            "comment_datefmt":"The date format string in UNIX date time structure format to convert CSV date into epoch time",
            "datefmt": "%b %d, %Y",
            "comment_lines_to_skip": "The number of lines to skip before getting into data row”,
            "lines_to_skip":1
        }
    }
    ~~~

2. To list your file type in the menu
edit the file _templates/type.html_.  
_e.g_ This is the entry for the above (_mysgr_) format in _templates/type.html_.

 `<input type="radio" name="filetype" value="mysgr"> My Sugr<br>`

#### Running the web application

> python plot_gluco.py
