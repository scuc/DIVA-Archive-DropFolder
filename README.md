# DIVA DMF DropFolder
A Python script for automating the creation of .csv. These files are used to trigger
DIVA Archive DMF service for archiving media objects (folder sets) to LTO tape. 

## Description
The script is used in conjunction with the [DIVAArchive](https://www.goecodigital.com) LTO library software. <br>

The DIVA DMF service is configured to monitor a drop folder location for .csv files. The .csv files are text files that act as the trigger for DIVA to begin archiving, and they contain all the
information related to the object that needs to be archived. <br><br>This script can be run with a cron job or with Windows Task Scheduler so that .csv files are generated automatically within a few minutes after a folder in placed in the drop folder. 

The DIVA portion of this workflow is not detailed or covered here.  

The script follows a series of steps: 


1. Check the queue of folder sets in the archive location. <br> If the folder count is above the set threshold (default = 10), <br> pause the script for 5min and then check again. Continue this loop <br> until the archive queue is below the allowed count. <br>
<br>
2. Create a list of new folder sets in the drop folder location(s). <br> If the length of the list is not zero, begin iterating over the list of set list. <br>
<br>
3. For each folder in the set list, check to the size to determine if the directory is still growing. <br> If the folder size is still growing after 90secs, move on the next directory on the list. <br>If it is not growing, move on to the next step. <br><br>
4. Walk the entire directory structure of each folder set, and <br> check each sub-directory and file name for illegal characters. <br> Replace or remove any illegal characters that are found. <br><br>
5. Generate the .csv trigger file for each folder in the list that has passed the preceeding steps. <br><br>
6. Move the .csv and its corresponding folder set into the archive location for DIVA to begin its archivng process. 

#### .csv example: 

		#
		# Object configuration
		#
	
		priority=50
		objectName=81187_SeriesName_SMLS_GRFX
		categoryName=AXF
	
		<comments>
		81187_SeriesName_SMLS_GRFX
		</comments>
	
		#sourceDestinationDIVA_Source_Dest=[source-dest name defined in the DIVA Config Utility]
		#sourceDestinationDIVAPath=\\UNC path to\DIVA\DropFolder\Location\
	
		<fileList>
		81187_SeriesName_SMLS_GRFX/*
		</fileList>

**priority** = default priority for the archive job (0 - 100), defaults to 50.<br>
**obejctName** = the name of the folder set. <br>
**categoryName** = the name of the DIVA tape Category, defined in the DIVA Config Utility<br>
**comments** = any comments relevant to the set, script defaults to the folder name.<br>
**sourceDestinationDIVA_Source_Dest** = the source-dest name defined in the DIVA Config Utility, not used in the .csv<br>
**sourceDestinationDIVAPath** = the UNC path defined in the DIVA Config Utility, not used in the .csv<br>
**fileList** = the files in the folder set that will be archived, uses an asterisk to include all file and folder paths in the entire directory.<br>

**NOTE:** DIVA_Source_Dest and DIVAPath are not used in the .csv because both of these values are constant and already defined in the Source-Destinations settings of the DIVA Config Utility.

## Prerequisites 

* Python 3.6 or higher
* [Diva Archive](https://www.goecodigital.com) 



## Files Included

* `main.py`
* `config.py`
* `dropfolder_check_csv.py`
* `logging.yaml `
* `check_dir_size.py`
* `archive_queue.py`


## Getting Started

* Install prerequisities 
* Create a `config.yaml` document with the format: 
&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  

&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; paths: &nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; script_root:&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; mac_root_path:&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; win_root_path:&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; drop_folder::&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; csv_dropfolder:&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; archiving:&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; error:&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; duplicates:&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; requires_zip:&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; win_archive::&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; DIVA_Source_Dest: &nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; DIVA_Obj_Category: &nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;    
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; urls: &nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; core_data_api:&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; core_manager_api:&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; creds: &nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; name:&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; password:&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp; 
 
* In the terminal cd to the source directory for the script and enter the command:<br>
&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp; `python main.py`
