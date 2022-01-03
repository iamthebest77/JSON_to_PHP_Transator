import json
from pprint import pprint
import sys
import datetime

today = datetime.datetime.now()
masterjson_file='masterasl.json';
out_file_name = "hotelbook_created.sql";
masterjson_data=open(masterjson_file);
parsed_masterjson = json.load(masterjson_data);

#------------------------------------------------------header--------------------------------------------------------------------#
str_sql = ""
str_table = ""
str_header = "-- Generated SQL Table Structures\n-- Author: Raunak, Sidharth\n-- Generation Time: " 
str_header += today.strftime("%d/%m/%Y %H:%M:%S")
str_header += "\n\nSET SQL_MODE = \"NO_AUTO_VALUE_ON_ZERO\";\nSET time_zone = \"+00:00\";"

#--------------------------------------------------table structure---------------------------------------------------------------#

for tablecount in range (0,len(parsed_masterjson['tables'])):
    str_table += "\n\n--\n-- Table structure for table `" + parsed_masterjson['tables'][tablecount]['name'] + "`\n--\n\n"
    str_table +="CREATE TABLE IF NOT EXISTS `" + parsed_masterjson['tables'][tablecount]['name'] + "` (\n"
                
    for attributecount in range (0, len(parsed_masterjson['tables'][tablecount]['attributes'])):
        isattributepresent = "no"
        for allattributescount in range (0, len(parsed_masterjson['attributes'])):
            if parsed_masterjson['attributes'][allattributescount]['name'] == parsed_masterjson['tables'][tablecount]['attributes'][attributecount]['column']:
                isattributepresent = "yes"
                tablename = parsed_masterjson['tables'][tablecount]['name']
                attributename = parsed_masterjson['attributes'][allattributescount]['name']
                type= parsed_masterjson['attributes'][allattributescount]['type']
                length= parsed_masterjson['attributes'][allattributescount]['length']
                default= parsed_masterjson['attributes'][allattributescount]['default']
                ifnull= parsed_masterjson['attributes'][allattributescount]['null']
                
                #**************************** setting default and null values*****************************#
                
                if default == "null":
                    default_value = "DEFAULT NULL"
                elif default == "none":
                    default_value = ""
                elif default == "current_timestamp":
                    default_value = "DEFAULT CURRENT_TIMESTAMP"
                else:
                    if type == "int":
                        default_value = "DEFAULT "+ default +" "
                    else:
                        default_value = "DEFAULT `"+ default +"` "

                if ifnull == "no":
                    null_value = "NOT NULL"
                else: 
                    null_value = ""
                #******************************************************************************************#
                
                if type == "int" or type == "int" or type == "varchar" or type == "char" :
                    str_table += "\t`"+ attributename + "` " + type + "(" + length + ") " + null_value +" "+ default_value + " ,\n"
                else : 
                    str_table += "\t`"+ attributename + "` " + type + " " + null_value + " " + default_value + " ,\n"
        
        if isattributepresent == "no":
            print "error : " + parsed_masterjson['tables'][tablecount]['attributes'][attributecount]['column']
            #sys.exit("Attribute mismatch : attribute mentioned in table description not present in all attributes list.")
    str_table = str_table.strip(" \n,")
    
    str_table += "\n\n) ENGINE=InnoDB DEFAULT CHARSET=latin1;"    
    
    
#-------------------------------------------------------------------handling foreign key, unique key and primary key constraints-------------------------------------#


str_alter = "\n\n--\n-- Indexes for dumped tables\n--\n\n"

for tablecount in range (0,len(parsed_masterjson['tables'])):
    tablename = parsed_masterjson['tables'][tablecount]['name']
    if len(parsed_masterjson['tables'][tablecount]['key_id']) == 0 and len(parsed_masterjson['tables'][tablecount]['unique_key_id']) == 0 :
        str_alter += ""
    else:
        str_alter +="ALTER TABLE `" + tablename + "`\n"
        
        for pkcount in range (0, len(parsed_masterjson['tables'][tablecount]['key_id'])):
            keyname = parsed_masterjson['tables'][tablecount]['key_id'][pkcount]['name']
            str_alter += "\tADD PRIMARY KEY (`" +  keyname + "`),\n"
        
        for uniquecount in range (0, len(parsed_masterjson['tables'][tablecount]['unique_key_id'])):
            uniquekeyname = parsed_masterjson['tables'][tablecount]['unique_key_id'][uniquecount]['name']
            str_alter += "\tADD UNIQUE KEY `" + uniquekeyname + "` (`" +  uniquekeyname + "`),\n"
        str_alter = str_alter.strip("\n,")
        str_alter += ";\n\n"

        
for tablecount in range (0,len(parsed_masterjson['tables'])):
    tablename = parsed_masterjson['tables'][tablecount]['name']
    if len(parsed_masterjson['tables'][tablecount]['foreign_key_id']) == 0:
        str_alter += ""
    else:
        str_alter +="ALTER TABLE `" + tablename + "`\n"
        for fkcount in range (0, len(parsed_masterjson['tables'][tablecount]['foreign_key_id'])):
            fkeyname = parsed_masterjson['tables'][tablecount]['foreign_key_id'][fkcount]['name']
            constraintname = parsed_masterjson['tables'][tablecount]['foreign_key_id'][fkcount]['constraintname']
            reftable = parsed_masterjson['tables'][tablecount]['foreign_key_id'][fkcount]['reftable']
            refcolumn = parsed_masterjson['tables'][tablecount]['foreign_key_id'][fkcount]['refcolumn']
            ondelete = parsed_masterjson['tables'][tablecount]['foreign_key_id'][fkcount]['ondelete']
            onupdate = parsed_masterjson['tables'][tablecount]['foreign_key_id'][fkcount]['onupdate']
            
            if ondelete == "restrict":
                ondelete_value = ""
            else :
                ondelete_value = "ON DELETE " + ondelete.upper()
            
            
            if onupdate == "restrict":
                onupdate_value = ""
            else :
                onupdate_value = "ON UPDATE " + onupdate.upper()
            
            str_alter += "\tADD CONSTRAINT `" +  constraintname + "` FOREIGN KEY (`" + fkeyname + "`) REFERENCES `" + reftable + "` (`" + refcolumn +  "`) " + ondelete_value + " " + onupdate_value + ",\n"
        str_alter = str_alter.strip("\n,")
        str_alter += ";\n"
        str_alter += "\n"
str_alter += "\n\n"
   
#----------------------------------------------writing to file and closing-------------------------------------------------------#

str_sql  += str_header + str_table + str_alter

text_file = open("hotelbook_created.sql", "w")
text_file.write("%s" % str_sql)
text_file.close()
masterjson_data.close();
