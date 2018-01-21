# Temperature-chart

Build charts based on temperature csv file.

This simple code based on Bokeh and reads csv file filed with temperatures from sensor readings. 

requirements: 
 - bokeh
 - pandas

how to use:
 - create an empty csv file. The first row should be: date,supply,return
 - then run following command from parent folder:

    python3 -m bokeh serve --address ip_address --allow-websocket-origin ip_address:portnr folder_name
