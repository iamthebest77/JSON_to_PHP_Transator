import json
from pprint import pprint
import sys
   
input_file = [line.rstrip('\n') for line in open('input_file.txt')]
json_file=input_file[0];
masterjson_file=input_file[1];

#json_file="studen_created.json";
#masterjson_file="academicmaster.json";

json_data=open(json_file);
masterjson_data=open(masterjson_file);
parsed_json = json.load(json_data);
parsed_masterjson = json.load(masterjson_data);


################### SQL PARSER (function to split and identify query) ##############################################
def splitquery(str):
    php_variable = []
    columns_list = []
    table_index = -1
    
    query_type = str.split(" ")
    #print "query_type " + query_type[0]

    ################## remember to throw error if query syntax is incorrect
    if query_type[0].lower() == "select" : 
        cols = str.split(" from ")
        from_split = cols[1]
        query_col_names = cols[0]
        
        find_tablename = str.split(" ")
        table_name_index = find_tablename.index("from") + 1
        table_name = from_split.split(" where ")
        having_clause = from_split.split(" having ")       ####### HAVING CODE ADDED
        #table = table_name[0].strip()
        table = find_tablename[table_name_index]
        #print "table name is " + table +"\n"
        
        istable_present = "no"
        
        for tablecheckcount in range (0,len(parsed_masterjson['tables'])) :
            if parsed_masterjson['tables'][tablecheckcount]['name'] == table :
                istable_present = "yes"
                table_index = tablecheckcount
                break
        
        #print "is table present : " + istable_present
        if istable_present == "no":
            print "ERROR : table name in the query '" + str + "' is incorrect or it is not specified in Master APL file"
            #sys.exit("ERROR : table name in the query '" + str + "' is incorrect or it is not specified in Master APL file")
            
        else:
            if query_type[0] + " *" in query_col_names : 
                ## fetch column names from master iff count(*) is not present in query
                for attributecount in range (0,len(parsed_masterjson['tables'][table_index]['attributes'])) :
                    str_col=parsed_masterjson['tables'][table_index]['attributes'][attributecount]['column']
                    columns_list.append(str_col);
            else :
                cols = query_col_names.split(query_type[0])
                #print " printing after split from query type " 
                #print cols
                colnames = cols[1].split(",")
                #print colnames
                #print " inside else " 
                for colcount in range (0,len(colnames)) :
                    if "as" in colnames[colcount] :                 ############ CODE FOR HANDLING ALIAS ADDED 
                        aliasname = colnames[colcount].split("as")
                        
                        if "sum" in aliasname[0] or "max" in aliasname[0] or "avg" in aliasname[0] or "min" in aliasname[0] or "count" in aliasname[0]:
                            actualcolnamelist = aliasname[0].split("(")
                            actualcolname = actualcolnamelist[1].strip()
                            actualcolname = actualcolname.strip(")")
                            actualcolname = actualcolname.strip()
                            iscolumn_present = "no"
                            for attributecheckcount in range (0,len(parsed_masterjson['tables'][table_index]['attributes'])) :
                                if actualcolname == parsed_masterjson['tables'][table_index]['attributes'][attributecheckcount]['column']:
                                    iscolumn_present = "yes"
                                    break
                                    
                            if iscolumn_present == "no":
                                print "ERROR : column name " + actualcolname + " in the query '" + str + "' is incorrect or it is not specified in Master APL file"
                                sys.exit("ERROR : column name " + actualcolname + " in the query '" + str + "' is incorrect or it is not specified in Master APL file")
                                
                        columns_list.append(aliasname[1].strip())
                        
                    else :
                        iscolumn_present = "no"
                        for attributecheckcount in range (0,len(parsed_masterjson['tables'][table_index]['attributes'])) :
                            if colnames[colcount].strip() == parsed_masterjson['tables'][table_index]['attributes'][attributecheckcount]['column']:
                                iscolumn_present = "yes"
                                break
                        #print "is column present : "+ iscolumn_present          
                        if iscolumn_present == "no":
                            print "ERROR : column name " + colnames[colcount].strip() + " in the query '" + str + "' is incorrect or it is not specified in Master APL file"
                            #sys.exit("ERROR : column name " + colnames[colcount].strip() + " in the query '" + str + "' is incorrect or it is not specified in Master APL file")
                        
                        columns_list.append(colnames[colcount].strip())
                        
            ############# Handling where clause 
            if len(table_name) > 1 :
                clauses = table_name[1].split(" and ")    
                #print clauses
                for clausecount in range (0, len(clauses)) :    
                    idandvalue = clauses[clausecount].split("=")
                    
                    if len(idandvalue) ==1:
                        idandvalue = clauses[clausecount].split(">")
                    
                    if len(idandvalue) ==1:
                        idandvalue = clauses[clausecount].split("<")
                        
                    if len(idandvalue) ==1:
                        idandvalue = clauses[clausecount].split("<>")
                        
                    if len(idandvalue) ==1:
                        idandvalue = clauses[clausecount].split(">=")
                        
                    if len(idandvalue) ==1:
                        idandvalue = clauses[clausecount].split("<=")
                        
                    variable= idandvalue[0].strip()
                    #print variable
                    value = idandvalue[1].strip()
                    #print value
                    ifgroupby = value.split(" group by ")
                    value = ifgroupby[0]
                    if "'$" in value[0:2] or " '$" in value[0:3] :
                        php_variable.append(value.strip(" '$"))
            #print "end of where"        
##################################### HAVING CODE ADDED ################################                    
            if len(having_clause) > 1 :
                havingclauses = having_clause[1].split(" and ")    
                #print clauses
                for havingclausecount in range (0, len(havingclauses)) :
                    havingidandvalue = havingclauses[havingclausecount].split("=")
        
                    if len(havingidandvalue) ==1:
                        havingidandvalue = havingclauses[havingclausecount].split(">")
                    
                    if len(havingidandvalue) ==1:
                        havingidandvalue = havingclauses[havingclausecount].split("<")
                        
                    if len(havingidandvalue) ==1:
                        havingidandvalue = havingclauses[havingclausecount].split("<>")
                        
                    if len(havingidandvalue) ==1:
                        havingidandvalue = havingclauses[havingclausecount].split(">=")
                        
                    if len(havingidandvalue) ==1:
                        havingidandvalue = havingclauses[havingclausecount].split("<=")

                    havingvariable= havingidandvalue[0].strip()
                    #print variable
                    havingvalue = havingidandvalue[1].strip()
                    #print value
                    if "'$" in havingvalue[0:2] or " '$" in havingvalue[0:3] :
                        php_variable.append(havingvalue.strip(" '$"))

    ## query type insert
    elif query_type[0].lower() == "insert" : 
        insert_cols=str.split("values")
        #print insert_cols[1]
        extracting_table = insert_cols[0].split("into")
        extracting_table = extracting_table[1].split("(")
        table = extracting_table[0].strip()
        #print "table name : " + table
        
        for tablecheckcount in range (0,len(parsed_masterjson['tables'])) :
            if parsed_masterjson['tables'][tablecheckcount]['name'] == table :
                istable_present = "yes"
                table_index = tablecheckcount
                break
                
        if istable_present == "no":
            print "ERROR : table name in the query '" + str + "' is incorrect or it is not specified in Master APL file"
            #sys.exit("ERROR : table name in the query '" + str + "' is incorrect or it is not specified in Master APL file")
            
        columncheck = extracting_table[1].strip(") ")
        
        columnchecklist = columncheck.split(",")
        
        iscolumn_present = "no"
        for columnchecklistcount in range(0, len(columnchecklist)):
            for attributecheckcount in range (0,len(parsed_masterjson['tables'][table_index]['attributes'])) :
                if columnchecklist[columnchecklistcount].strip() == parsed_masterjson['tables'][table_index]['attributes'][attributecheckcount]['column']:
                    iscolumn_present = "yes"
                    break
                        
            if iscolumn_present == "no":
                print "ERROR : column name " + columnchecklist[columnchecklistcount] + " in the query '" + str + "' is incorrect or it is not specified in Master APL file"
                #sys.exit("ERROR : column name " + columnchecklist[columnchecklistcount] + " in the query '" + str + "' is incorrect or it is not specified in Master APL file")

        else :
            i_c_stripped=insert_cols[1].strip(" ( ")
            i_c_stripped=i_c_stripped.strip(" ) ")
            insert_columns_list= i_c_stripped.split(",")
            #print insert_columns_list
            for colcount in range (0, len(insert_columns_list)):
                if "'$" in insert_columns_list[colcount][0:2] or " '$" in insert_columns_list[colcount][0:3] :
                    variable= insert_columns_list[colcount].strip()
                    php_variable.append(variable.strip(" '$"))
        
    ##query type delete
    elif query_type[0].lower() == "delete" :
    
        extracting_table = str.split(" from ")
        from_split = extracting_table[1]
        table_name = from_split.split(" where ")
        table = table_name[0].strip()

        istable_present = "no"
        
        for tablecheckcount in range (0,len(parsed_masterjson['tables'])) :
            if parsed_masterjson['tables'][tablecheckcount]['name'] == table :
                istable_present = "yes"
                table_index = tablecheckcount
                break
                
        if istable_present == "no":
            print "ERROR : table name in the query '" + str + "' is incorrect or it is not specified in Master APL file"
            #sys.exit("ERROR : table name in the query '" + str + "' is incorrect or it is not specified in Master APL file")
            
        delete_split = str.split(" where ")
        if len(delete_split) > 1 :
            clauses = delete_split[1].split(" and ")    
            #print clauses
            for clausecount in range (0, len(clauses)) :
                idandvalue = clauses[clausecount].split("=")

                if len(idandvalue) ==1:
                    idandvalue = clauses[clausecount].split(">")
                
                if len(idandvalue) ==1:
                    idandvalue = clauses[clausecount].split("<")
                    
                if len(idandvalue) ==1:
                    idandvalue = clauses[clausecount].split("<>")
                    
                if len(idandvalue) ==1:
                    idandvalue = clauses[clausecount].split(">=")
                    
                if len(idandvalue) ==1:
                    idandvalue = clauses[clausecount].split("<=")
                    
                variable= idandvalue[0].strip()
                #print variable
                value = idandvalue[1].strip()
                #print value
                
                iscolumn_present = "no"
                for attributecheckcount in range (0,len(parsed_masterjson['tables'][table_index]['attributes'])) :
                    if variable == parsed_masterjson['tables'][table_index]['attributes'][attributecheckcount]['column']:
                        iscolumn_present = "yes"
                        break
                            
                if iscolumn_present == "no":
                    print "ERROR : column name " + variable + " in the query '" + str + "' is incorrect or it is not specified in Master APL file"
                    #sys.exit("ERROR : column name " + variable + " in the query '" + str + "' is incorrect or it is not specified in Master APL file")

                
                if "'$" in value[0:2] or " '$" in value[0:3] :
                    php_variable.append(value.strip(" '$"))

    ##query type update
    elif query_type[0].lower() == "update" :
        update_split_set = str.split(" set ")
        update_split_where = update_split_set[1].split(" where ")
        
        extracting_table = update_split_set[0].split(" ")
        table = extracting_table[1].strip()

        istable_present = "no"
        
        for tablecheckcount in range (0,len(parsed_masterjson['tables'])) :
            if parsed_masterjson['tables'][tablecheckcount]['name'] == table :
                istable_present = "yes"
                table_index = tablecheckcount
                break
                
        if istable_present == "no":
            print "ERROR : table name in the query '" + str + "' is incorrect or it is not specified in Master APL file"
            #sys.exit("ERROR : table name in the query '" + str + "' is incorrect or it is not specified in Master APL file")
        
        if len(update_split_where) > 1 :
            clauses = update_split_where[1].split(" and ")    
            #print clauses
            for clausecount in range (0, len(clauses)) :
                idandvalue = clauses[clausecount].split("=")
                
                if len(idandvalue) ==1:
                    idandvalue = clauses[clausecount].split(">")
                
                if len(idandvalue) ==1:
                    idandvalue = clauses[clausecount].split("<")
                    
                if len(idandvalue) ==1:
                    idandvalue = clauses[clausecount].split("<>")
                    
                if len(idandvalue) ==1:
                    idandvalue = clauses[clausecount].split(">=")
                    
                if len(idandvalue) ==1:
                    idandvalue = clauses[clausecount].split("<=")
                
                variable= idandvalue[0].strip()
                #print variable
                value = idandvalue[1].strip()
                
                iscolumn_present = "no"
                for attributecheckcount in range (0,len(parsed_masterjson['tables'][table_index]['attributes'])) :
                    if variable == parsed_masterjson['tables'][table_index]['attributes'][attributecheckcount]['column']:
                        iscolumn_present = "yes"
                        break
                            
                if iscolumn_present == "no":
                    print "ERROR : column name " + variable + " in the query '" + str + "' is incorrect or it is not specified in Master APL file"
                    #sys.exit("ERROR : column name " + variable + " in the query '" + str + "' is incorrect or it is not specified in Master APL file")
                
                #print value
                if "'$" in value[0:2] or " '$" in value[0:3] :
                    php_variable.append(value.strip(" '$"))
    
        update_split = update_split_where[0].split(",")
        for update_split_count in range(0, len(update_split)) :
            idandvalue = update_split[update_split_count].split("=")
            variable= idandvalue[0].strip()
            #print variable
            value = idandvalue[1].strip()
            
            iscolumn_present = "no"
            for attributecheckcount in range (0,len(parsed_masterjson['tables'][table_index]['attributes'])) :
                if variable == parsed_masterjson['tables'][table_index]['attributes'][attributecheckcount]['column']:
                    iscolumn_present = "yes"
                    break
                        
            if iscolumn_present == "no":
                print "ERROR : column name " + variable + " in the query '" + str + "' is incorrect or it is not specified in Master APL file"
                #sys.exit("ERROR : column name " + variable + " in the query '" + str + "' is incorrect or it is not specified in Master APL file")
            
            #print value
            if "'$" in value[0:2] or " '$" in value[0:3] :
                php_variable.append(value.strip(" '$"))
                
    else:
        print "ERROR : query type is invalid : " + str
        #sys.exit("ERROR : query type is invalid : " + str)
    ###### throw error that query is incorrect
    
    return query_type[0].lower(),list(set(php_variable)), list(set(columns_list))

# query split function definition ends here


str_tabspace = "\t"

str_host = "<?php \n define ('DB_HOST', '" + parsed_masterjson['connect_parameters']['DB_HOST'].strip() + "');";
str_dbuser = "\n define ('DB_USER', '" + parsed_masterjson['connect_parameters']['DB_USER'].strip() + "');";
str_dbpassword = "\n define ('DB_PASSWORD', '" + parsed_masterjson['connect_parameters']['DB_PASSWORD'].strip() + "');";
str_dbname = "\n define ('DB_NAME', '" + parsed_masterjson['connect_parameters']['DB_NAME'].strip() + "');\n ?>" ;

str_connect= str_host + str_dbuser +str_dbpassword + str_dbname; ##### print this in connect.inc.php
#print to connect.inc.php
text_file = open("connect.inc.php", "w")
text_file.write("%s" % str_connect)
text_file.close()

text_fileht = open("C:\\xampp\\htdocs\\Includes\\connect.inc.php", "w")
text_fileht.write("%s" % str_connect)
text_fileht.close()

str_php =" <?php \n " + str_tabspace + "ob_start();\n\tsession_start();\n\tinclude_once($_SERVER['DOCUMENT_ROOT']. '/Includes/connect.inc.php');\n\t$db=mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die('Error connecting to MySQL server.'); \n\n" 

for initcount in range(0, len (parsed_json['php']['initialize'])) :
    if parsed_json['php']['initialize'][initcount]['value'] == "empty" :
        str_php += "\t$_SESSION['" + parsed_json['php']['initialize'][initcount]['name'] + "'] = \"\"; \n" 
    else :
        str_php += "\t$_SESSION['" + parsed_json['php']['initialize'][initcount]['name'] + "'] = " + parsed_json['php']['initialize'][initcount]['value'] + "; \n" 

for initcount in range(0, len (parsed_json['php']['initialize'])) :
    if parsed_json['php']['initialize'][initcount]['value'] == "empty" :
        str_php += "\t$" + parsed_json['php']['initialize'][initcount]['name'] + " = \"\"; \n" 
    else :
        str_php += "\t$" + parsed_json['php']['initialize'][initcount]['name'] + " = " + parsed_json['php']['initialize'][initcount]['value'] + "; \n" 

        
#------handling session variables from master file---------
for sessioncount in range(0, len (parsed_masterjson['session_parameters'])) :
    session_var = parsed_masterjson['session_parameters'][sessioncount]['name']
    str_php += "\t$"+ session_var +" = $_SESSION['" + session_var + "']; \n"

    
#----------------initialize queries-----------------
for querycount in range(0, len (parsed_json['php']['query'])) :
    querytype, variablelist, columnlist = splitquery(parsed_json['php']['query'][querycount]['queryexpression'])
    
        
    str_php += "\t\t$sqlquery = \"" + parsed_json['php']['query'][querycount]['queryexpression'] + "\"; \n"
    
    ####### if querytpe is insert or delete or update
    if querytype != "select":
        str_php += "\t\tif(mysqli_query($db,$sqlquery)) { } \n"
    
    ####### if querytype is select then retrieve the column values from table
    else :
        str_php += "\t\t$data = mysqli_query($db,$sqlquery); \n\t\twhile($row=mysqli_fetch_array($data)) { \n"
        
        for collistcount in range(0, len(columnlist)) :
            str_php += "\t\t\t$" + columnlist[collistcount] + " = $row['" + columnlist[collistcount] + "']; \n"
            
        #######closing while
        str_php += "\t\t}"
    
    for collistcount in range(0, len(columnlist)) :
        for initializecount in range(0, len(parsed_json['php']['initialize'])):
            if columnlist[collistcount] == parsed_json['php']['initialize'][initializecount]['name']:
                str_php += "\t\t$_SESSION['" + columnlist[collistcount] + "'] = $" + columnlist[collistcount] + "; \n"
            
        
####handling submit buttons
str_php += "\tif(isset($_POST['submit']))\n\t{\n"

str_php_button = ""
processed_buttons_list = []


#for html head code
str_head_javascript="<html>\n<head>\n\n<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js\"></script>\n<script type=\"text/javascript\">\n"
str_head_ajax=""

javascript_function_list = []       #####################  list to store the validation functions called by inout tags of current from


#for html body code
str_html = "\n<body>\n\n\t<div style=\"margin-left:100px\">";

# html links print
count =0;
for count in range(0, len (parsed_json['html']['links'])) :
    str_links = "\t<a href=\""+ parsed_json['html']['links'][count]['target_page'] + "\" style=\"position:absolute; left: " +  parsed_json['html']['links'][count]['x-coordinate'] + "px; top:" + parsed_json['html']['links'][count]['y-coordinate'] + "px;\">"+parsed_json['html']['links'][count]['label']+"</a>";
    str_html += "\n" + str_links

str_html += "<br><br>" + "\n\t</div>\n\n"
    
# html form print
count =0;
str_form =""

#------------------------------------- Initializing HTMLPRINT input tags -------------------------

  
str_htmlprint_input_id =""
str_htmlprint_input_name = ""
str_htmlprint_input_type = ""
str_htmlprint_input_display_name = ""
str_htmlprint_input_newline = ""
str_htmlprint_input_placeholder = ""
str_htmlprint_input_required = ""
str_htmlprint_input_value = ""
str_htmlprint_input_readonly = ""
str_htmlprint_input_fieldaction = ""
str_htmlprint_input_functiontype = ""
str_htmlprint_input_functionname = ""
str_htmlprint_input_display_name_label = "" 
str_htmlprint_input_start = ""
str_htmlprint_input_type_print = ""
str_htmlprint_input_id_print = ""
str_htmlprint_input_name_print = ""
str_htmlprint_input_placeholder_print = "" 
str_htmlprint_input_end = "" 
#--------------------------------------
############################################# ITERATING THROUGH FORMS ARRAY  ################################

for count in range(0, len (parsed_json['html']['forms'])) :
    inputcount =0
    validation_function_list = []
    if parsed_json['html']['forms'][count]['action'] == "self" :
        formaction = "<?php echo $_SERVER['PHP_SELF'] ?>"
    else:
        formaction = parsed_json['html']['forms'][count]['action'];
        
    formname = parsed_json['html']['forms'][count]['name'].strip()
    formmethod = parsed_json['html']['forms'][count]['method'].strip()
    formclass = parsed_json['html']['forms'][count]['class'].strip()
    formlabel = parsed_json['html']['forms'][count]['label'].strip()
    formvalidation_function = parsed_json['html']['forms'][count]['validation_function'].strip()
    formname = parsed_json['html']['forms'][count]['name'].strip()
    
    if formvalidation_function=="":
        str_form +="\t<form class=\""+formclass+"\" name=\""+formname+"\" method=\""+formmethod+"\" action=\""+formaction+"\"><br><br><br>\n";
        str_head_validation = ""
    
    else:
        
        str_form +="\t<form class=\""+formclass+"\" name=\""+formname+"\" method=\""+formmethod+"\" onsubmit= \"return " + formvalidation_function + "()\" action=\""+formaction+"\"><br><br><br>\n";
        
        ##### Checking if the formvalidation_function has already been created by any form previously
        if formvalidation_function in validation_function_list :
            str_head_validation = ""
        else :
            str_head_validation = "\nfunction " + formvalidation_function + "()\n\t{\n"  ## remember to close it in the end
        
    str_form_input="";
    
    ##### iterating through form input fields array
    for inputcount in range(0, len (parsed_json['html']['forms'][count]['form_input_fields'])) :
    
        str_input_id = parsed_json['html']['forms'][count]['form_input_fields'][inputcount]['id'].strip()
        str_input_name = str_input_id
        str_input_type = parsed_json['html']['forms'][count]['form_input_fields'][inputcount]['type'].strip()
        str_input_display_name = parsed_json['html']['forms'][count]['form_input_fields'][inputcount]['name'].strip()
        str_input_newline = parsed_json['html']['forms'][count]['form_input_fields'][inputcount]['newline'].strip()
        str_input_placeholder = parsed_json['html']['forms'][count]['form_input_fields'][inputcount]['placeholder'].strip()
        str_input_required = parsed_json['html']['forms'][count]['form_input_fields'][inputcount]['required'].strip()
        str_input_validation = parsed_json['html']['forms'][count]['form_input_fields'][inputcount]['validation'].strip()
        str_input_value = parsed_json['html']['forms'][count]['form_input_fields'][inputcount]['value'].strip()
        str_input_readonly = parsed_json['html']['forms'][count]['form_input_fields'][inputcount]['readonly'].strip()
        str_input_fieldaction = parsed_json['html']['forms'][count]['form_input_fields'][inputcount]['fieldaction'].strip()
        str_input_functiontype = parsed_json['html']['forms'][count]['form_input_fields'][inputcount]['functiontype'].strip()
        str_input_functionname = parsed_json['html']['forms'][count]['form_input_fields'][inputcount]['functionname'].strip()
        
        ##### handling 'input tag start print' 
        str_input_start = "<input "
        
        ##### handling 'input tag end print' 
        str_input_end = " />"
        
        ##### handling 'required' 
        if str_input_required == "no":
            str_input_required =""
        else:
            str_input_required =" required "
            
        ##### handling 'type print' 
        str_input_type_print = " type = \"" + str_input_type + "\" "
        
        ##### handling 'display name label print' 
        str_input_display_name_label = "<label>"+ str_input_display_name +"\t</label>"
        
        ##### handling 'placeholder print' 
        str_input_placeholder_print = " placeholder = \"" + str_input_placeholder + "\" "
        
        ##### handling 'name print' 
        str_input_name_print = " name = \"" + str_input_name + "\" "
        
        ##### handling 'id print' 
        str_input_id_print = " id = \"" + str_input_id + "\" "    
        
            
        ##### handling 'readonly' 
        if str_input_readonly == "no":
            str_input_readonly =""
        else:
            str_input_readonly =" readonly = \"\" "
            
        ##### handling 'newline' 
        if str_input_newline == "no":
            str_input_newline ="&emsp;"
        else:
            str_input_newline ="<br><br>"
            
        ##### handling 'value' 
        if str_input_value == "":
            str_input_value =""
        
        elif "text(" in str_input_value[0:5] :
            str_input_value = " value=\"" + str_input_value[5: (len(str_input_value) - 1) ] + "\" "
            
        elif "text (" in str_input_value[0:6] :
            str_input_value = " value=\"" + str_input_value[6: (len(str_input_value) - 1) ] + "\" "
            
        elif "," in str_input_value :
            str_input_value_temp = " value=\"<?php echo htmlentities("
            str_input_valuelist = str_input_value.split(",");
            str_input_value =""
        
            for str_input_valuelength in range(0, len(str_input_valuelist)) :
                ispresent ="no"
                for valuelength in range (0,len(parsed_json['php']['initialize'])):
                    if parsed_json['php']['initialize'][valuelength]['name'] == str_input_valuelist[str_input_valuelength].strip() :
                        str_input_value += "$_SESSION['" + str_input_valuelist[str_input_valuelength].strip() + "'].','."
                        ispresent = "yes"
                        break
                if ispresent == "no":
                    str_input_value += "$" + str_input_valuelist[str_input_valuelength].strip() + ".','."
                        
            str_input_value = str_input_value.strip(".','.")
            str_input_value += "); ?>\" "
            str_input_value_temp += str_input_value
            str_input_value = str_input_value_temp
                                          
        else:
            ispresent = "no"
            for valuelength in range (0,len(parsed_json['php']['initialize'])):
                if parsed_json['php']['initialize'][valuelength]['name'] == str_input_value :
                    str_input_value = " value=\"<?php echo htmlentities($_SESSION['" + str_input_value + "']); ?>\" "
                    ispresent ="yes"
                    break
            if ispresent == "no" :
                str_input_value = " value=\"<?php echo htmlentities($" + str_input_value + "); ?>\" "
            
        ##### handling 'field validation!!!  Modifying str_head_validation string'
        
        ##### Do not generate validation code if formvalidation_function has already been created by any form previously
        if formvalidation_function not in validation_function_list :
            validation_function_list.append(formvalidation_function)

        if not(str_input_validation == "no" or str_input_validation == ""):
            
            if str_input_validation in parsed_masterjson['javascript']:
                print str_input_validation  
                ##### handling user defined validation functions            
                if parsed_masterjson['javascript'][str_input_validation]['user_defined'] == "yes":
                
                    user_validation_file = parsed_masterjson['javascript'][str_input_validation]['filename']
                    with open(user_validation_file, "r") as v_file:
                        data = v_file.read()
                    str_head_validation += data
                    
                ##### string validation function
                elif str_input_validation == "validate_string" :
                    validate_minlength = parsed_masterjson['javascript'][str_input_validation]['min_length']
                    validate_maxlength = parsed_masterjson['javascript'][str_input_validation]['max_length']
                    validate_specialchars = parsed_masterjson['javascript'][str_input_validation]['special_chars']
                    validate_digit = parsed_masterjson['javascript'][str_input_validation]['digit']
                    validate_alphabet = parsed_masterjson['javascript'][str_input_validation]['alphabet']
                
                    str_head_validation += "\t\tvar "+ str_input_id + " = document.getElementById(\""+ str_input_id + "\").value;\n"
                    
                    str_head_validation += "\t\tif(" + str_input_id + ".length > " + validate_maxlength + " || " + str_input_id + ".length < " + validate_minlength + ")\n\t\t\t{\n\t\t\t\talert(\" String Lenght Inappropriate\");\n\t\t\t\treturn false; \n\t\t\t}\n"
                    
                    if validate_specialchars == "no":
                        str_head_validation += "\t\tif(/[@()~`!#$%\^&*+=\-\[\]\\';,/{}|\\\":<>\?]/g.test(" + str_input_id + "))\n\t\t\t{\n\t\t\t\talert(\"Special character not allowed!!\");\n\t\t\t\treturn false; \n\t\t\t}\n"
                        
                    if validate_digit == "no":
                        str_head_validation += "\t\tif(/[0123456789]/g.test(" + str_input_id + "))\n\t\t\t{\n\t\t\t\talert(\"Digits not allowed!!\");\n\t\t\t\treturn false; \n\t\t\t}\n"
                        
                    if validate_alphabet == "no":
                        str_head_validation += "\t\tif(/[qwertyuiopasdfghjklzxcvbnm]/g.test(" + str_input_id + "))\n\t\t\t{\n\t\t\t\talert(\"Alphabets not allowed!!\");\n\t\t\t\treturn false; \n\t\t\t}\n"
                
                ##### Name validation function
                elif str_input_validation == "validate_name" :
                    validate_minlength = parsed_masterjson['javascript'][str_input_validation]['min_length']
                    validate_maxlength = parsed_masterjson['javascript'][str_input_validation]['max_length']
                    validate_specialchars = parsed_masterjson['javascript'][str_input_validation]['special_chars']
                    validate_digit = parsed_masterjson['javascript'][str_input_validation]['digit']
                    validate_alphabet = parsed_masterjson['javascript'][str_input_validation]['alphabet']
                
                    str_head_validation += "\t\tvar "+ str_input_id + " = document.getElementById(\""+ str_input_id + "\").value;\n"
                    
                    str_head_validation += "\t\tif(" + str_input_id + ".length > " + validate_maxlength + " || " + str_input_id + ".length < " + validate_minlength + ")\n\t\t\t{\n\t\t\t\talert(\" String Length Inappropriate\");\n\t\t\t\treturn false; \n\t\t\t}\n"
                    
                    if validate_specialchars == "no":
                        str_head_validation += "\t\tif(/[@()~`!#$%\^&*+=\-\[\]\\';,/{}|\\\":<>\?]/g.test(" + str_input_id + "))\n\t\t\t{\n\t\t\t\talert(\"Special character not allowed!!\");\n\t\t\t\treturn false; \n\t\t\t}\n"
                        
                    if validate_digit == "no":
                        str_head_validation += "\t\tif(/[0123456789]/g.test(" + str_input_id + "))\n\t\t\t{\n\t\t\t\talert(\"Digits not allowed!!\");\n\t\t\t\treturn false; \n\t\t\t}\n"
                        
                    if validate_alphabet == "no":
                        str_head_validation += "\t\tif(/[qwertyuiopasdfghjklzxcvbnm]/g.test(" + str_input_id + "))\n\t\t\t{\n\t\t\t\talert(\"Alphabets not allowed!!\");\n\t\t\t\treturn false; \n\t\t\t}\n"
                        
                ##### emailid validation function
                elif str_input_validation == "validate_emailid" :
                    validate_minlength = parsed_masterjson['javascript'][str_input_validation]['min_length']
                    validate_maxlength = parsed_masterjson['javascript'][str_input_validation]['max_length']
                
                    str_head_validation += "\t\tvar "+ str_input_id + " = document.getElementById(\""+ str_input_id + "\").value;\n"
                    
                    str_head_validation += "\t\tif(" + str_input_id + ".length > " + validate_maxlength + " || " + str_input_id + ".length < " + validate_minlength + ")\n\t\t\t{\n\t\t\t\talert(\" String Length Inappropriate\");\n\t\t\t\treturn false; \n\t\t\t}\n"
                    
                    str_head_validation += "\t\tvar atpos=" + str_input_id + ".indexOf(\"@\"); \n\t\tvar dotpos=" + str_input_id + ".lastIndexOf(\".\"); \n\t\tif (atpos<1 || dotpos<atpos+2 || dotpos+2>=" + str_input_id + ".length) \n\t\t\t{ \n\t\t\t\talert(\"Invalid e-mail address\"); \n\t\t\t\treturn false; \n\t\t\t} \n"
                        
                    
                ##### integer validation function
                elif str_input_validation == "validate_integer" :
                    validate_minlength = parsed_masterjson['javascript'][str_input_validation]['min_length']
                    validate_maxlength = parsed_masterjson['javascript'][str_input_validation]['max_length']
                
                    str_head_validation += "\t\tvar "+ str_input_id + " = document.getElementById(\""+ str_input_id + "\").value;\n"
                    
                    str_head_validation += "\t\tif(" + str_input_id + ".length > " + validate_maxlength + " || " + str_input_id + ".length < " + validate_minlength + ")\n\t\t\t{\n\t\t\t\talert(\" String Length Inappropriate\");\n\t\t\t\treturn false; \n\t\t\t}\n"
                    
                    str_head_validation += "\t\tif(isNaN(" + str_input_id + "))\n\t\t\t{\n\t\t\t\talert(\"Please enter a valid number\");\n\t\t\t\treturn false; \n\t\t\t}\n"
                    
                ##### date validation function
                elif str_input_validation == "validate_date" or str_input_validation == "validate_exparrdate" or str_input_validation == "validate_expdepdate" or str_input_validation == "validate_actarrdate" or str_input_validation == "validate_actdepdate" :
                    validate_minvalue = parsed_masterjson['javascript'][str_input_validation]['min_value']
                    validate_maxvalue = parsed_masterjson['javascript'][str_input_validation]['max_value']
                
                    str_head_validation += "\t\tvar "+ str_input_id + " = new Date(document.getElementById(\""+ str_input_id + "\").value);\n"
                    
                    ##### define javascript date variable if given date depending on masterasl is empty or not
                    ##### define javascript date variable if both mindate and maxdate present
                    if validate_minvalue != "" and validate_maxvalue != "" :
                        if validate_minvalue == "system_date" :
                            str_head_validation += "\t\tvar minDate = new Date();\n"
                        else:
                            str_head_validation += "\t\tvar minDate = new Date(document.getElementById(\"" + validate_minvalue + "\").value);\n"
                        
                        if validate_maxvalue == "system_date" :
                            str_head_validation += "\t\tvar maxDate = new Date();\n"
                        else:
                            str_head_validation += "\t\tvar maxDate = new Date(document.getElementById(\"" + validate_maxvalue + "\").value);\n"
                        
                        str_head_validation += "\t\tif( "+ str_input_id + " < minDate || "+ str_input_id + " > maxDate) \n\t\t\t{ \n\t\t\t\talert(\" Date Inappropriate \"); \n\t\t\t\treturn false; \n\t\t\t} \n"
                    
                    ##### define javascript date variable if only mindate present
                    elif validate_minvalue != "" and validate_maxvalue == "" :
                        if validate_minvalue == "system_date" :
                            str_head_validation += "\t\tvar minDate = new Date();\n"
                        else:
                            str_head_validation += "\t\tvar minDate = new Date('" + validate_minvalue + "');\n"
                            
                        str_head_validation += "\t\tif( "+ str_input_id + " < minDate) \n\t\t\t{ \n\t\t\t\talert(\" Date Inappropriate \"); \n\t\t\t\treturn false; \n\t\t\t} \n"
                    
                    ##### define javascript date variable if only maxdate present                   
                    elif validate_minvalue == "" and validate_maxvalue != "" :
                        if validate_maxvalue == "system_date" :
                            str_head_validation += "\t\tvar maxDate = new Date();\n"
                        else:
                            str_head_validation += "\t\tvar maxDate = new Date('" + validate_maxvalue + "');\n"
                            
                        str_head_validation += "\t\tif( "+ str_input_id + " > maxDate) \n\t\t\t{ \n\t\t\t\talert(\" Date Inappropriate \"); \n\t\t\t\treturn false; \n\t\t\t} \n"
                    
                    ##### define javascript date variable if both mindate and maxdate not present   
                    else:
                        print "both mindate and maxdate not present in masterasl file"
                        sys.exit("both mindate and maxdate not present in masterasl file")
                            
            else:
                print "input validation name given by user is not present in masterasl file"
                sys.exit("input validation name given by user is not present in masterasl file")
        
        
        ##### handling 'field validation finished here!!!  Modified str_head_validation string'
        
        
        ############################ handling function type and fieldaction begins!!! ######################################
        if str_input_functiontype == "no":
            str_input_functiontype = ""
        
        elif str_input_functiontype == "ajax":
            str_input_functiontype = ""
            #### ajax code modified here
            if str_head_ajax == "" :
                str_head_ajax += "\n$(document).ready(function(){\n"
                
            str_head_ajax += "\t$(\"#" + str_input_functionname + "\")." + str_input_fieldaction + "(function(){\n"
            
            for retrievedfieldcount in range(0, len (parsed_json['ajax'][str_input_functionname]['retrieved_fields'])) :
                str_head_ajax += "\t\tvar " + parsed_json['ajax'][str_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + " = $(\"#" + parsed_json['ajax'][str_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + "\").val();\n"
                                                                                
            str_head_ajax += "\t\t$.ajax({\n\t\t\ttype : \"" + parsed_json['ajax'][str_input_functionname]['type'] + "\",\n\t\t\turl : \"" + parsed_json['ajax'][str_input_functionname]['scriptfilename'] + "\",\n\t\t\tdataType : \"" + parsed_json['ajax'][str_input_functionname]['dataType'] + "\",\n"
                
            str_head_ajax += "\t\t\tdata: "
            retrievedfieldcount = 0
            for retrievedfieldcount in range(0, len (parsed_json['ajax'][str_input_functionname]['retrieved_fields']) -1 ) :
                str_head_ajax += "'" + parsed_json['ajax'][str_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + "='+" + parsed_json['ajax'][str_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + ", "
            
            if len(parsed_json['ajax'][str_input_functionname]['retrieved_fields']) == 1 :
                str_head_ajax += "'" + parsed_json['ajax'][str_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + "='+" + parsed_json['ajax'][str_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + ",\n"
            
            if len(parsed_json['ajax'][str_input_functionname]['retrieved_fields']) > 1 :
                str_head_ajax += "'" + parsed_json['ajax'][str_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + "='+" + parsed_json['ajax'][str_input_functionname]['retrieved_fields'][retrievedfieldcount + 1]['fieldname'] + ",\n"
                                                                                        
            str_head_ajax += "\t\t\tsuccess: function(data , data1, textstatus) {\n\t\t\t\tif(data) { \n"
            
            ###### handling single return data
            if parsed_json['ajax'][str_input_functionname]['success']['returndata'] == "single":
                for outputfieldcount in range(0, len (parsed_json['ajax'][str_input_functionname]['success']['outputlocations']) ) :
                
                    ###### printing when output type is field
                    if parsed_json['ajax'][str_input_functionname]['success']['outputlocations'][outputfieldcount]['type'] == "field" :
                        str_head_ajax += "\t\t\t\t\t$('#" + parsed_json['ajax'][str_input_functionname]['success']['outputlocations'][outputfieldcount]['location'] + "').val(data);\n"   
                    
                    ###### printing when output type is html
                    else :
                        str_head_ajax += "\t\t\t\t\t$('#" + parsed_json['ajax'][str_input_functionname]['success']['outputlocations'][outputfieldcount]['location'] + "').html(data);\n"

            ###### handling multiple return data
            else :
                str_head_ajax += "\t\t\t\t\tvar splitdata = data.split( '" + parsed_json['ajax'][str_input_functionname]['success']['delimiter'] + "');\n"
                
                for outputfieldcount in range(0, len (parsed_json['ajax'][str_input_functionname]['success']['outputlocations']) ) :
                
                    ###### printing when output type is field
                    if parsed_json['ajax'][str_input_functionname]['success']['outputlocations'][outputfieldcount]['type'] == "field" :
                        str_head_ajax += "\t\t\t\t\t$('#" + parsed_json['ajax'][str_input_functionname]['success']['outputlocations'][outputfieldcount]['location'] + "').val(splitdata[" + str(outputfieldcount + 1) +"]);\n" 
                    
                    ###### printing when output type is html
                    else :
                        str_head_ajax += "\t\t\t\t\tvar totaldata;\n\t\t\t\t\tfor(var i = 1; i < splitdata.length; i++) {\n\t\t\t\t\t\tvar ele = splitdata[i];\n\t\t\t\t\t\ttotaldata = totaldata+ele+\"<br/>\";\n\t\t\t\t\t}\n";
                        str_head_ajax += "\t\t\t\t\t$('#" + parsed_json['ajax'][str_input_functionname]['success']['outputlocations'][outputfieldcount]['location'] + "').html(totaldata);\n"
                                                                                                
            str_head_ajax += "}\n\t\t\t\telse { \n\t\t\t\t\talert( ' ajax error ' ); \n\t\t\t\t} \n\t\t\t} \n\t\t}); \n\t}); \n "
            
            
            
            ###################################### creating ajax script file and writing content in it    ##################################################
            
            str_ajax_script = "<?php \n\tinclude_once($_SERVER['DOCUMENT_ROOT']. '/Includes/connect.inc.php'); \n\t$db = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die('Error connecting to MySQL server.'); \n"
            
            for retrievedfieldcount in range(0, len (parsed_json['ajax'][str_input_functionname]['retrieved_fields']) ) :
                str_ajax_script += "\t$" + parsed_json['ajax'][str_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + " = $_" + parsed_json['ajax'][str_input_functionname]['type'] + "['" + parsed_json['ajax'][str_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + "']; \n"

            str_ajax_script += "\t$query = \"" + parsed_json['ajax'][str_input_functionname]['queryexpression'] + "\";\n"
            
            str_ajax_script += "\t$data = mysqli_query($db,$query); \n\tif(mysqli_num_rows($data)==1) { \n\t\twhile($row=mysqli_fetch_array($data)) { \n"
            
            scriptquerytype,scriptvariablelist,scriptcolumnlist = splitquery(parsed_json['ajax'][str_input_functionname]['queryexpression'])
            
            for scriptquerycount in range(0,len(scriptcolumnlist)):
                str_ajax_script += "\t\t\t$" + scriptcolumnlist[scriptquerycount] + " = $row['" + scriptcolumnlist[scriptquerycount] + "']; \n"
            
            str_ajax_script += "\n\t\t} \n\t} \n"
            
            if parsed_json['ajax'][str_input_functionname]['success']['outputlocations'][outputfieldcount]['type'] == "field" :
                for outputfieldcount in range(0,len(parsed_json['ajax'][str_input_functionname]['success']['outputlocations'])):
                    if parsed_json['ajax'][str_input_functionname]['success']['delimiter'] != "nil" :
                        str_ajax_script += "\techo('" + parsed_json['ajax'][str_input_functionname]['success']['delimiter'] + "'); \n"
                    str_ajax_script += "\techo($" + parsed_json['ajax'][str_input_functionname]['success']['outputlocations'][outputfieldcount]['location'] + "); \n"         
            
            else:
                for scriptcolumnlistcount in range(0,len(scriptcolumnlist)):
                    if parsed_json['ajax'][str_input_functionname]['success']['delimiter'] != "nil" :
                        str_ajax_script += "\techo('" + parsed_json['ajax'][str_input_functionname]['success']['delimiter'] + "'); \n"
                    str_ajax_script += "\techo($" + scriptcolumnlist[scriptcolumnlistcount] + "); \n"
                
                
            str_ajax_script += "?>"
            
            
            ajaxscriptfile = parsed_json['ajax'][str_input_functionname]['scriptfilename']
            text_file = open(ajaxscriptfile, "w")
            text_file.write("%s" % str_ajax_script)
            text_file.close()
            
            text_fileht = open("C:\\xampp\\htdocs\\"+ ajaxscriptfile, "w")
            text_fileht.write ("%s" % str_ajax_script)
            text_fileht.close()
        
        else:
            ########## handling javascript function call and arguments which is to be printed inside input tag
            str_input_functiontype = " on" + str_input_fieldaction + " = \"" + str_input_functionname + "( "
            argcount = 0
            if parsed_json['javascript'][str_input_functionname]['source'] == "self" :
                for argcount in range(0, len(parsed_json['javascript'][str_input_functionname]['arguments'])) :
                    str_input_functiontype += parsed_json['javascript'][str_input_functionname]['arguments'][argcount]['argname'] + ", "
                
                str_input_functiontype = str_input_functiontype.strip(", ")
            str_input_functiontype += ")\" "
                
                
            #### javascript head code modified here
            if str_input_functionname not in javascript_function_list :                         
                javascript_function_list.append(str_input_functionname)
                str_javascript_temp = ""
                ####### if javascript function is user defined
                if parsed_json['javascript'][str_input_functionname]['source'] != "self" :
                    user_javascript_file = parsed_json['javascript'][str_input_functionname]['source']
                    with open(user_javascript_file, "r") as j_file:
                        data = j_file.read()
                    str_javascript_temp += "\n"+data +"\n"
                    j_file.close()
                        
                ####### if javascript function is not user defined
                else :
                    str_javascript_temp += "\nfunction " + str_input_functionname +"("
                    ####### printing javascript function arguments
                    argcount = 0
                    for argcount in range(0, len(parsed_json['javascript'][str_input_functionname]['arguments'])) :
                        str_javascript_temp += parsed_json['javascript'][str_input_functionname]['arguments'][argcount]['argname'] + ", "
                    
                    str_javascript_temp = str_javascript_temp.strip(", ")
                    str_javascript_temp += ") \n\t{\n"
                        
                    for varcount in range(0, len(parsed_json['javascript'][str_input_functionname]['retrieved_fields'])) :
                        str_javascript_temp += "\t\tvar " +  parsed_json['javascript'][str_input_functionname]['retrieved_fields'][varcount]['fieldname'] + " = document.getElementById(\"" + parsed_json['javascript'][str_input_functionname]['retrieved_fields'][varcount]['fieldname'] + "\").value;\n"
                    
                    ####### printing default values of fields
                    for expressioncount in range(0, len(parsed_json['javascript'][str_input_functionname]['expressions'])) :
                        str_exp_target_field = parsed_json['javascript'][str_input_functionname]['expressions'][expressioncount]['target_field']
                        str_default_value = parsed_json['javascript'][str_input_functionname]['expressions'][expressioncount]['default_value']
                        #str_javascript_temp += "\t\tvar " + str_exp_target_field + " = " + parsed_json['javascript'][str_input_functionname]['expressions'][expressioncount]['expression'] + ";\n"
                        str_javascript_temp += "\t\tdocument.getElementById('" + str_exp_target_field + "').value = "+str_default_value+";\n"
                        
                    ####### handling the if block
                    str_if_case_handle = "\t\tif( "
                    for varcount in range(0, len(parsed_json['javascript'][str_input_functionname]['retrieved_fields'])) :
                        str_current_var = parsed_json['javascript'][str_input_functionname]['retrieved_fields'][varcount]['fieldname']
                        str_current_lowerbound = parsed_json['javascript'][str_input_functionname]['retrieved_fields'][varcount]['lowerbound']
                        str_current_upperbound = parsed_json['javascript'][str_input_functionname]['retrieved_fields'][varcount]['upperbound']
                        
                        ########### handling upperbound and lowerbound to print the if statement
                        if str_current_lowerbound != "nil" :
                            str_if_case_handle += str_current_var + " > " + str_current_lowerbound + " && "
                        
                        if str_current_upperbound != "nil" :
                            str_if_case_handle += str_current_var + " < " + str_current_upperbound + " && "
                            
                
                        ########### handling not allowed and mandatory values to print the if statement
                        for notallowedcount in range(0, len(parsed_json['javascript'][str_input_functionname]['retrieved_fields'][varcount]['notallowed'])) :
                            if parsed_json['javascript'][str_input_functionname]['retrieved_fields'][varcount]['notallowed'][notallowedcount]['value'] != "empty":
                                str_if_case_handle += str_current_var + " != " + parsed_json['javascript'][str_input_functionname]['retrieved_fields'][varcount]['notallowed'][notallowedcount]['value'] + " && "
                            else :
                                str_if_case_handle += str_current_var + " != \"\" && "
                    
                        for mandatorycount in range(0, len(parsed_json['javascript'][str_input_functionname]['retrieved_fields'][varcount]['mandatory'])) :
                            if parsed_json['javascript'][str_input_functionname]['retrieved_fields'][varcount]['mandatory'][mandatorycount]['value'] != "empty":
                                str_if_case_handle += str_current_var + " != " + parsed_json['javascript'][str_input_functionname]['retrieved_fields'][varcount]['mandatory'][mandatorycount]['value'] + " && "
                            else :
                                str_if_case_handle += str_current_var + " != \"\" && "
                                
                        str_if_case_handle = str_if_case_handle[:-3]     ##### removing the last two extra && symbols from if statement
                        
                        
                        #### handling the case when there is no condition in IF 
                        if (str_current_lowerbound == "nil" and str_current_upperbound == "nil" and len(parsed_json['javascript'][str_input_functionname]['retrieved_fields'][varcount]['notallowed']) == 0 and len(parsed_json['javascript'][str_input_functionname]['retrieved_fields'][varcount]['mandatory']) == 0) :
                            str_if_case_handle += "true "
                            
                    str_if_case_handle += ") \n\t\t\t{ \n"
                        
                    ########### printing the expression inside if statement         
                    for expressioncount in range(0, len(parsed_json['javascript'][str_input_functionname]['expressions'])) :
                        str_exp_target_field = parsed_json['javascript'][str_input_functionname]['expressions'][expressioncount]['target_field']
                        str_if_case_handle += "\t\t\t\tvar " + str_exp_target_field + " = " + parsed_json['javascript'][str_input_functionname]['expressions'][expressioncount]['expression'] + ";\n"
                        str_if_case_handle += "\t\t\t\tdocument.getElementById('" + str_exp_target_field + "').value = "+str_exp_target_field+"; \n"
                        
                    str_if_case_handle += "\t\t\t}"
                    
                    ## closing javascript function and adding to str_javascript_temp
                    str_javascript_temp += str_if_case_handle + "\n\t}\n" 
                        
                str_head_javascript += str_javascript_temp
                
        ################################## PRINTING INPUT FIELDS ###################################################
        
        #### handling input type plaintext
        if str_input_type == "plaintext" :
            str_form_input += "\t\t" + str_input_display_name + "&emsp;&emsp;" + str_input_newline + "\n"

        ######################## if input tag is print , then handle printfields and printhtmlfields ###############################
        elif str_input_type == "print" :
            ###### opening php tag only once if it is not opened already
            if len(processed_buttons_list) == 0:
                str_form_input += "\t\t<?php \n\t\t\tif(isset($_POST['submit'])) { \n"
            for buttoncount in range(0, len (parsed_json['html']['forms'][count]['button'])) :
                str_button_displayname = parsed_json['html']['forms'][count]['button'][buttoncount]['displayname']
                str_button_name = parsed_json['html']['forms'][count]['button'][buttoncount]['name']
                str_button_type = parsed_json['html']['forms'][count]['button'][buttoncount]['type']
                str_button_newline = parsed_json['html']['forms'][count]['button'][buttoncount]['newline']
                str_button_x_coordinate = parsed_json['html']['forms'][count]['button'][buttoncount]['x-coordinate']
                str_button_y_coordinate = parsed_json['html']['forms'][count]['button'][buttoncount]['y-coordinate']
                str_button_value = str_button_displayname

                printfieldlist = []     ######## list to store the field which have the same prinpositions as the print id given in input tag
                htmlprintfieldlist = [] ######## list to store the html field which have the same prinpositions as the print id given in input tag
                printfieldnewlinelist = []
                printhtmlfieldnewlinelist =[]
                for printfieldcount in range(0, len (parsed_json['html']['forms'][count]['button'][buttoncount]['printfields'])) :
                    if parsed_json['html']['forms'][count]['button'][buttoncount]['printfields'][printfieldcount]['printposition'] == str_input_id :
                        printfieldlist.append(parsed_json['html']['forms'][count]['button'][buttoncount]['printfields'][printfieldcount]['fieldname'])
                        printfieldnewlinelist.append(parsed_json['html']['forms'][count]['button'][buttoncount]['printfields'][printfieldcount]['newline'])
                        
                for printhtmlfieldcount in range(0, len (parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'])) :
                    if parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][printhtmlfieldcount]['printposition'] == str_input_id :
                        htmlprintfieldlist.append(parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][printhtmlfieldcount]['fieldname'])
                        printhtmlfieldnewlinelist.append(parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][printhtmlfieldcount]['newline'])
                        
                
                if len(printfieldlist) != 0 or len(htmlprintfieldlist) != 0 :
                    ## add button to processed list 
                    processed_buttons_list.append(str_button_displayname)
                    
                    ##handling button queries
                    str_form_input += "\t\t\t\tif($_POST['submit']==\"" + str_button_value + "\"){\n"
                    
                    ###### iterating through query expression array
                    for querycount in range(0, len (parsed_json['html']['forms'][count]['button'][buttoncount]['query'])) :
                        querytype, variablelist, columnlist = splitquery(parsed_json['html']['forms'][count]['button'][buttoncount]['query'][querycount]['queryexpression'])
                        
                        for varlistcount in range(0, len(variablelist)) :
                            str_form_input += "\t\t\t\t\t$" + variablelist[varlistcount] + " = $_POST['" + variablelist[varlistcount] + "']; \n"
                            
                        #for retaincount in range(0, len (parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'])) :
                            #str_form_input += "\t\t\t\t\t$_SESSION['" + parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'][retaincount]['fieldname'] + "'] = $" + parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'][retaincount]['fieldname'] + "; \n"

                        
                        str_form_input += "\t\t\t\t\t$sqlquery = \"" + parsed_json['html']['forms'][count]['button'][buttoncount]['query'][querycount]['queryexpression'] + "\"; \n"
                        
                        ####### if querytpe is insert or delete or update
                        if querytype != "select":
                            str_form_input += "\t\t\t\t\tif(mysqli_query($db,$sqlquery)){} \n"
                        
                        ####### if querytype is select then retrieve the column values from table
                        else :
                            str_form_input += "\t\t\t\t\t$data = mysqli_query($db,$sqlquery); \n \t\t\t\t\twhile($row=mysqli_fetch_array($data)) { \n"
                            
                            for collistcount in range(0, len(columnlist)) :
                                str_form_input += "\t\t\t\t\t\t$" + columnlist[collistcount] + " = $row['" + columnlist[collistcount] + "']; \n"
                                
                            
                            str_form_input += "\t\t?>\n"
                            """
                            for printfieldcount in range (0, len(printfieldlist)):
                                newline_print = printfieldnewlinelist[printfieldcount].strip()
                                if newline_print == "no":
                                    str_form_input += "\t\t<?php echo $" + printfieldlist[printfieldcount] + "; ?>&emsp;&emsp;&emsp;\n"
                                else:   
                                    str_form_input += "\t\t<?php echo $" + printfieldlist[printfieldcount] + "; ?><br><br>\n"
                            """
                                
################################################# html field print and ajax/ javascript function handling code for htmlprint field list starts here         ################################################# 
                            for htmlprintfieldcount in range (0, len(parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'])):
                            
                                if parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][htmlprintfieldcount]['fieldname'] in htmlprintfieldlist:
                                
                                    str_htmlprint_input_id = parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][htmlprintfieldcount]['fieldname'].strip()
                                    str_htmlprint_input_name = str_htmlprint_input_id
                                    str_htmlprint_input_type = parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][htmlprintfieldcount]['type'].strip()
                                    str_htmlprint_input_display_name = parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][htmlprintfieldcount]['name'].strip()
                                    str_htmlprint_input_newline = parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][htmlprintfieldcount]['newline'].strip()
                                    str_htmlprint_input_placeholder = parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][htmlprintfieldcount]['placeholder'].strip()
                                    str_htmlprint_input_required = parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][htmlprintfieldcount]['required'].strip()
                                    str_htmlprint_input_value = parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][htmlprintfieldcount]['value'].strip()
                                    str_htmlprint_input_readonly = parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][htmlprintfieldcount]['readonly'].strip()
                                    str_htmlprint_input_fieldaction = parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][htmlprintfieldcount]['fieldaction'].strip()
                                    str_htmlprint_input_functiontype = parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][htmlprintfieldcount]['functiontype'].strip()
                                    str_htmlprint_input_functionname = parsed_json['html']['forms'][count]['button'][buttoncount]['printhtmlfields'][htmlprintfieldcount]['functionname'].strip()
                                    
                                    print str_htmlprint_input_name
                                    
                                    ##### handling 'input tag start print' 
                                    str_htmlprint_input_start = "<input "
                                    
                                    ##### handling 'input tag end print' 
                                    str_htmlprint_input_end = " />"
                                    
                                    ##### handling 'required' 
                                    if str_htmlprint_input_required == "no":
                                        str_htmlprint_input_required =""
                                    else:
                                        str_htmlprint_input_required =" required "
                                        
                                    ##### handling 'type print' 
                                    str_htmlprint_input_type_print = " type = \"" + str_htmlprint_input_type + "\" "
                                    
                                    ##### handling 'display name label print' 
                                    str_htmlprint_input_display_name_label = "<label>"+ str_htmlprint_input_display_name +"\t</label>"
                                    
                                    ##### handling 'placeholder print' 
                                    str_htmlprint_input_placeholder_print = " placeholder = \"" + str_htmlprint_input_placeholder + "\" "
                                    
                                    ##### handling 'name print' 
                                    str_htmlprint_input_name_print = " name = \"" + str_htmlprint_input_name + "\" "
                                    
                                    ##### handling 'id print' 
                                    str_htmlprint_input_id_print = " id = \"" + str_htmlprint_input_id + "\" "    
                                    
                                        
                                    ##### handling 'readonly' 
                                    if str_htmlprint_input_readonly == "no":
                                        str_htmlprint_input_readonly =""
                                    else:
                                        str_htmlprint_input_readonly =" readonly = \"\" "
                                        
                                    ##### handling 'newline' 
                                    if str_htmlprint_input_newline == "no":
                                        str_htmlprint_input_newline ="&emsp;"
                                    else:
                                        str_htmlprint_input_newline ="<br><br>"
                                        
                                    ##### handling 'value' 

                                    if "text(" in str_htmlprint_input_value[0:5] :
                                        str_htmlprint_input_value = " value = \"" + str_htmlprint_input_value[5: (len(str_htmlprint_input_value) - 1) ] + "\" "
                                        
                                    elif "text (" in str_htmlprint_input_value[0:6] :
                                        str_htmlprint_input_value = " value = \"" + str_htmlprint_input_value[6: (len(str_htmlprint_input_value) - 1) ] + "\" "
                                        
                                    elif "," in str_htmlprint_input_value :
                                        str_htmlprint_input_value_temp = " value=\"<?php echo htmlentities("
                                        str_htmlprint_input_valuelist = str_htmlprint_input_value.split(",");
                                        str_htmlprint_input_value =""
                                    
                                        for str_htmlprint_input_valuelength in range(0, len(str_htmlprint_input_valuelist)) :
                                            ispresentinretain = "no"
                                            for htmlprint_retain_count in range(0,len (parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'])) :
                                                if str_htmlprint_input_valuelist[str_htmlprint_input_valuelength].strip(" '.$") == parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'][htmlprint_retain_count]['fieldname'] :
                                                    str_htmlprint_input_value += "$_SESSION['" + str_htmlprint_input_valuelist[str_htmlprint_input_valuelength].strip() + "'].','."
                                                    ispresentinretain = "yes"
                                                    
                                            if ispresentinretain == "no" :
                                                str_htmlprint_input_value += "$" + str_htmlprint_input_valuelist[str_htmlprint_input_valuelength].strip() + ".','."
                                                
                                        str_htmlprint_input_value = str_htmlprint_input_value.strip(".','.")
                                        str_htmlprint_input_value += "); ?>\" "
                                        str_htmlprint_input_value_temp += str_htmlprint_input_value
                                        str_htmlprint_input_value = str_htmlprint_input_value_temp
                                        
                                    else:
                                        str_value_temp = str_htmlprint_input_value
                                        str_htmlprint_input_value = " value=\"<?php echo htmlentities("
                                        ispresentinretain = "no"
                                        for htmlprint_retain_count in range(0,len (parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'])) :
                                            
                                            if str_htmlprint_input_id == parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'][htmlprint_retain_count]['fieldname'] :
                                                str_htmlprint_input_value += "$_SESSION['" + str_value_temp.strip() + "']"
                                                ispresentinretain = "yes"
                                                
                                        if ispresentinretain == "no" :
                                            str_htmlprint_input_value += "$" + str_value_temp.strip()
                                        
                                        str_htmlprint_input_value += "); ?>\" "
                                        
                                        
                                    ############################ handling function type and fieldaction begins!!! ######################################
                                    if str_htmlprint_input_functiontype == "no":
                                        str_htmlprint_input_functiontype = ""
                                    
                                    elif str_htmlprint_input_functiontype == "ajax":
                                        str_htmlprint_input_functiontype = ""
                                        #### ajax code modified here
                                        if str_head_ajax == "" :
                                            str_head_ajax += "$(document).ready(function(){\n"
                                            

                                        str_head_ajax += "\t$(\"#" + str_htmlprint_input_functionname + "\")." + str_htmlprint_input_fieldaction + "(function(){\n"
                                        
                                        for htmlprint_retrievedfieldcount in range(0, len (parsed_json['ajax'][str_htmlprint_input_functionname]['retrieved_fields'])) :
                                            str_head_ajax += "\t\tvar " + parsed_json['ajax'][str_htmlprint_input_functionname]['retrieved_fields'][htmlprint_retrievedfieldcount]['fieldname'] + " = $(\"#" + parsed_json['ajax'][str_htmlprint_input_functionname]['retrieved_fields'][htmlprint_retrievedfieldcount]['fieldname'] + "\").val();\n"
                                                                                                            
                                        str_head_ajax += "\t\t$.ajax(\n{\n type : \"" + parsed_json['ajax'][str_htmlprint_input_functionname]['type'] + "\",\n\t\turl : \"" + parsed_json['ajax'][str_htmlprint_input_functionname]['scriptfilename'] + "\",\n\t\tdataType : \"" + parsed_json['ajax'][str_htmlprint_input_functionname]['dataType'] + "\",\n"
                                            
                                        str_head_ajax += "\t\tdata: "
                                        retrievedfieldcount = 0
                                        for retrievedfieldcount in range(0, len (parsed_json['ajax'][str_htmlprint_input_functionname]['retrieved_fields']) -1 ) :
                                            str_head_ajax += "'" + parsed_json['ajax'][str_htmlprint_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + "='+" + parsed_json['ajax'][str_htmlprint_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + ", "
                                        
                                        if len(parsed_json['ajax'][str_htmlprint_input_functionname]['retrieved_fields']) == 1 :
                                            str_head_ajax += "'" + parsed_json['ajax'][str_htmlprint_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + "='+" + parsed_json['ajax'][str_htmlprint_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + ",\n"
                                        
                                        if len(parsed_json['ajax'][str_htmlprint_input_functionname]['retrieved_fields']) > 1 :
                                            str_head_ajax += "'" + parsed_json['ajax'][str_htmlprint_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + "='+" + parsed_json['ajax'][str_htmlprint_input_functionname]['retrieved_fields'][retrievedfieldcount + 1]['fieldname'] + ",\n"
                                                                                                                    
                                        str_head_ajax += "\t\tsuccess: function(data , data1, textstatus) {\n\t\t\tif(data){ \n"
                                        
                                        ###### handling single return data
                                        if parsed_json['ajax'][str_htmlprint_input_functionname]['success']['returndata'] == "single":
                                            for outputfieldcount in range(0, len (parsed_json['ajax'][str_htmlprint_input_functionname]['success']['outputlocations']) ) :
                                            
                                                ###### printing when output type is field
                                                if parsed_json['ajax'][str_htmlprint_input_functionname]['success']['outputlocations'][outputfieldcount]['type'] == "field" :
                                                    str_head_ajax += "\t\t\t\t$('#" + parsed_json['ajax'][str_htmlprint_input_functionname]['success']['outputlocations'][outputfieldcount]['location'] + "').val(data);\n"   
                                                
                                                ###### printing when output type is html
                                                else :
                                                    str_head_ajax += "\t\t\t\t$('#" + parsed_json['ajax'][str_htmlprint_input_functionname]['success']['outputlocations'][outputfieldcount]['location'] + "').html(data);\n"

                                        ###### handling multiple return data
                                        else :
                                            str_head_ajax += "\t\t\t\tvar splitdata = data.split( '" + parsed_json['ajax'][str_htmlprint_input_functionname]['success']['delimiter'] + "');\n"
                                            
                                            for outputfieldcount in range(0, len (parsed_json['ajax'][str_htmlprint_input_functionname]['success']['outputlocations']) ) :
                                            
                                                ###### printing when output type is field
                                                if parsed_json['ajax'][str_htmlprint_input_functionname]['success']['outputlocations'][outputfieldcount]['type'] == "field" :
                                                    str_head_ajax += "\t\t\t\t$('#" + parsed_json['ajax'][str_htmlprint_input_functionname]['success']['outputlocations'][outputfieldcount]['location'] + "').val(splitdata[" + str(outputfieldcount + 1) +"]);\n" 
                                                
                                                ###### printing when output type is html
                                                else :
                                                    str_head_ajax += "\t\t\t\t\tvar totaldata;\n\t\t\t\t\tfor(var i = 1; i < splitdata.length; i++) {\n\t\t\t\t\t\tvar ele = splitdata[i];\n\t\t\t\t\t\ttotaldata = totaldata+ele+\"<br/>\";\n\t\t\t\t\t}\n";
                                                    str_head_ajax += "\t\t\t\t\t$('#" + parsed_json['ajax'][str_htmlprint_input_functionname]['success']['outputlocations'][outputfieldcount]['location'] + "').html(totaldata);\n"
                                                                                                                            
                                        str_head_ajax += "}\n else { \n\t\t\t\talert( ' ajax error ' ); \n\t\t\t} \n\t\t} \n\t}); \n }); \n "
                                        
                                        
                                        
                                        ###################################### creating ajax script file and writing content in it    ##################################################
                                        
                                        str_ajax_script = "<?php \n include_once($_SERVER['DOCUMENT_ROOT']. '/Includes/connect.inc.php'); \n $db = mysqli_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME) or die('Error connecting to MySQL server.'); \n "
                                        
                                        for retrievedfieldcount in range(0, len (parsed_json['ajax'][str_htmlprint_input_functionname]['retrieved_fields']) ) :
                                            str_ajax_script += "$" + parsed_json['ajax'][str_htmlprint_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + " = $_" + parsed_json['ajax'][str_htmlprint_input_functionname]['type'] + "['" + parsed_json['ajax'][str_input_functionname]['retrieved_fields'][retrievedfieldcount]['fieldname'] + "']; \n "

                                        str_ajax_script += "$query = \"" + parsed_json['ajax'][str_htmlprint_input_functionname]['queryexpression'] + "\";\n"
                                        
                                        str_ajax_script += "$data = mysqli_query($db,$query); \n if(mysqli_num_rows($data)==1)  \n  { \n  while($row=mysqli_fetch_array($data)) \n  { \n"
                                        
                                        scriptquerytype,scriptvariablelist,scriptcolumnlist = splitquery(parsed_json['ajax'][str_htmlprint_input_functionname]['queryexpression'])
                                        
                                        for scriptquerycount in range(0,len(scriptcolumnlist)):
                                            str_ajax_script += "$" + scriptcolumnlist[scriptquerycount] + " = $row['" + scriptcolumnlist[scriptquerycount] + "']; \n "
                                        
                                        str_ajax_script += "\n } \n } \n"
                                        
                                        if parsed_json['ajax'][str_htmlprint_input_functionname]['success']['outputlocations'][outputfieldcount]['type'] == "field" :
                                            for outputfieldcount in range(0,len(parsed_json['ajax'][str_htmlprint_input_functionname]['success']['outputlocations'])):
                                                if parsed_json['ajax'][str_htmlprint_input_functionname]['success']['delimiter'] != "nil" :
                                                    str_ajax_script += "echo('" + parsed_json['ajax'][str_htmlprint_input_functionname]['success']['delimiter'] + "'); \n"
                                                str_ajax_script += "echo($" + parsed_json['ajax'][str_htmlprint_input_functionname]['success']['outputlocations'][outputfieldcount]['location'] + "); \n "         
                                            
                                        
                                        else:
                                            for scriptcolumnlistcount in range(0,len(scriptcolumnlist)):
                                                if parsed_json['ajax'][str_htmlprint_input_functionname]['success']['delimiter'] != "nil" :
                                                    str_ajax_script += "echo('" + parsed_json['ajax'][str_htmlprint_input_functionname]['success']['delimiter'] + "'); \n"
                                                str_ajax_script += "echo($" + scriptcolumnlist[scriptcolumnlistcount] + "); \n "         
                                        
                                        str_ajax_script += "?>"
                                        
                                        
                                        ajaxscriptfile = parsed_json['ajax'][str_htmlprint_input_functionname]['scriptfilename']
                                        text_file = open(ajaxscriptfile, "w")
                                        text_file.write("%s" % str_ajax_script)
                                        text_file.close()
                                        
                                        text_fileht = open("C:\\xampp\\htdocs\\"+ ajaxscriptfile, "w")
                                        text_fileht.write ("%s" % str_ajax_script)
                                        text_fileht.close()
                                    
                                    else:
                                        ########## handling javascript function call and arguments which is to be printed inside input tag
                                        str_htmlprint_input_functiontype = " on" + str_htmlprint_input_fieldaction + " = \"" + str_htmlprint_input_functionname + "( "
                                        argcount = 0
                                        if parsed_json['javascript'][str_htmlprint_input_functionname]['source'] == "self" :
                                            for argcount in range(0, len(parsed_json['javascript'][str_htmlprint_input_functionname]['arguments'])) :
                                                str_htmlprint_input_functiontype += parsed_json['javascript'][str_htmlprint_input_functionname]['arguments'][argcount]['argname'] + ", "
                                            
                                            str_htmlprint_input_functiontype = str_htmlprint_input_functiontype.strip(", ")
                                        str_htmlprint_input_functiontype += ")\" "
                                            
                                        #### javascript head code modified here
                                        if str_htmlprint_input_functionname not in javascript_function_list :
                                            javascript_function_list.append(str_htmlprint_input_functionname)
                               
                                            str_javascript_temp = ""
                                            ####### if javascript function is user defined
                                            if parsed_json['javascript'][str_htmlprint_input_functionname]['source'] != "self" :
                                                user_javascript_file = parsed_json['javascript'][str_htmlprint_input_functionname]['source']
                                                with open(user_javascript_file, "r") as j_file:
                                                    data = j_file.read()
                                                str_javascript_temp += "\n"+data +"\n"
                                                j_file.close()
                                                    
                                            ####### if javascript function is not user defined
                                            else :
                                                str_javascript_temp += "\nfunction " + str_htmlprint_input_functionname +"("
                                                ####### printing javascript function arguments
                                                argcount = 0
                                                for argcount in range(0, len(parsed_json['javascript'][str_htmlprint_input_functionname]['arguments']) -1) :
                                                    str_javascript_temp += parsed_json['javascript'][str_htmlprint_input_functionname]['arguments'][argcount]['argname'] + ", "
                                                
                                                str_javascript_temp = str_javascript_temp.strip(", ")
                                                str_javascript_temp += ") \n { \n"
                                                    
                                                for varcount in range(0, len(parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'])) :
                                                    str_javascript_temp += "var " +  parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'][varcount]['fieldname'] + " = document.getElementById(\"" + parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'][varcount]['fieldname'] + "\").value;\n"
                                                
                                                ####### printing default values of fields
                                                for expressioncount in range(0, len(parsed_json['javascript'][str_htmlprint_input_functionname]['expressions'])) :
                                                    str_exp_target_field = parsed_json['javascript'][str_htmlprint_input_functionname]['expressions'][expressioncount]['target_field']
                                                    str_javascript_temp += "var " + str_exp_target_field + " = " + parsed_json['javascript'][str_htmlprint_input_functionname]['expressions'][expressioncount]['expression'] + ";\n"
                                                    str_javascript_temp += "document.getElementById('" + str_exp_target_field + "').value = "+str_exp_target_field+"; \n"
                                                    
                                                ####### handling the if block
                                                str_if_case_handle = "if( "
                                                for varcount in range(0, len(parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'])) :
                                                    str_current_var = parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'][varcount]['fieldname']
                                                    str_current_lowerbound = parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'][varcount]['lowerbound']
                                                    str_current_upperbound = parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'][varcount]['upperbound']
                                                    
                                                    ########### handling upperbound and lowerbound to print the if statement
                                                    if str_current_lowerbound != "nil" :
                                                        str_if_case_handle += str_current_var + " > " + str_current_lowerbound + " && "
                                                    
                                                    if str_current_upperbound != "nil" :
                                                        str_if_case_handle += str_current_var + " < " + str_current_upperbound + " && "
                                                        
                                            
                                                    ########### handling not allowed and mandatory values to print the if statement
                                                    for notallowedcount in range(0, len(parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'][varcount]['notallowed'])) :
                                                        if parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'][varcount]['notallowed'][notallowedcount]['value'] != "empty":
                                                            str_if_case_handle += str_current_var + " != " + parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'][varcount]['notallowed'][notallowedcount]['value'] + " && "
                                                        else :
                                                            str_if_case_handle += str_current_var + " != \"\" && "
                                                
                                                    for mandatorycount in range(0, len(parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'][varcount]['mandatory'])) :
                                                        if parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'][varcount]['mandatory'][mandatorycount]['value'] != "empty":
                                                            str_if_case_handle += str_current_var + " != " + parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'][varcount]['mandatory'][mandatorycount]['value'] + " && "
                                                        else :
                                                            str_if_case_handle += str_current_var + " != \"\" && "
                                                            
                                                    str_if_case_handle = str_if_case_handle[:-3]     ##### removing the last two extra && symbols from if statement
                                                    
                                                    
                                                    #### handling the case when there is no condition in IF 
                                                    if (str_current_lowerbound == "nil" and str_current_upperbound == "nil" and len(parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'][varcount]['notallowed']) == 0 and len(parsed_json['javascript'][str_htmlprint_input_functionname]['retrieved_fields'][varcount]['mandatory']) == 0) :
                                                        str_if_case_handle += "true "
                                                        
                                                str_if_case_handle += ") \n { \n"
                                                    
                                                ########### printing the expression inside if statement         
                                                for expressioncount in range(0, len(parsed_json['javascript'][str_htmlprint_input_functionname]['expressions'])) :
                                                    str_exp_target_field = parsed_json['javascript'][str_htmlprint_input_functionname]['expressions'][expressioncount]['target_field']
                                                    str_if_case_handle += "var " + str_exp_target_field + " = " + parsed_json['javascript'][str_htmlprint_input_functionname]['expressions'][expressioncount]['expression'] + ";\n"
                                                    str_if_case_handle += "document.getElementById('" + str_exp_target_field + "').value = "+str_exp_target_field+"; \n"
                                                    
                                                str_if_case_handle += "} \n"
                                                
                                                ## closing javascript function and adding to str_javascript_temp
                                                str_javascript_temp += str_if_case_handle + "\n}\n" 
                                            str_head_javascript += str_javascript_temp
                                    """
                                    if str_htmlprint_input_type != "submit":
                                        str_form_input += "\t\t" + str_htmlprint_input_display_name_label + str_htmlprint_input_start + str_htmlprint_input_type_print + str_htmlprint_input_id_print + str_htmlprint_input_name_print + str_htmlprint_input_placeholder_print + str_htmlprint_input_value + str_htmlprint_input_required + str_htmlprint_input_readonly + str_htmlprint_input_functiontype + str_htmlprint_input_end + str_htmlprint_input_newline + "\n"
                                    
                                    else:
                                        str_form_input += "\t\t<button type=\"submit\" name = \"" + str_htmlprint_input_name + "\" " + str_htmlprint_input_value  + str_htmlprint_input_functiontype + ">" + str_htmlprint_input_display_name + "</button>" + str_htmlprint_input_newline + "\n"
                                    """
################################################# html field print and ajax/ javascript function handling code for htmlprint field list ends here           #################################################                                   

                            ##### Closing while loop of query
                            str_form_input += "\t\t<?php\n\t\t\t\t\t}\n"
                                
                        #for retaincount in range(0, len (parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'])) :
                         #   str_form_input += "\t\t\t\t\t$_SESSION['" + parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'][retaincount]['fieldname'] + "'] = $" + parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'][retaincount]['fieldname'] + "; \n"

                        for collistcount in range(0, len(columnlist)) :
                            for initializecount in range(0, len(parsed_json['php']['initialize'])):
                                if columnlist[collistcount] == parsed_json['php']['initialize'][initializecount]['name']:
                                    str_form_input += "\t\t$_SESSION['" + columnlist[collistcount] + "'] = $" + columnlist[collistcount] + "; \n"
                    
                    
                    for retaincount in range(0, len (parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'])) :
                        str_form_input += "\t\t\t\t\t$_SESSION['" + parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'][retaincount]['fieldname'] + "'] = $" + parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'][retaincount]['fieldname'] + "; \n"
                    
                    
                    if str_htmlprint_input_type != "submit":
                        str_form_input += "\t\t?>" + str_htmlprint_input_display_name_label + str_htmlprint_input_start + str_htmlprint_input_type_print + str_htmlprint_input_id_print + str_htmlprint_input_name_print + str_htmlprint_input_placeholder_print + str_htmlprint_input_value + str_htmlprint_input_required + str_htmlprint_input_readonly + str_htmlprint_input_functiontype + str_htmlprint_input_end + str_htmlprint_input_newline + "\n"
                    
                    else:
                        str_form_input += "\t\t?>\n\t\t<button type=\"submit\" name = \"" + str_htmlprint_input_name + "\" " + str_htmlprint_input_value  + str_htmlprint_input_functiontype + ">" + str_htmlprint_input_display_name + "</button>" + str_htmlprint_input_newline + "\n"
                    
                    for printfieldcount in range (0, len(printfieldlist)):
                        newline_print = printfieldnewlinelist[printfieldcount].strip()
                        if newline_print == "no":
                            str_form_input += "\t\t<?php echo $" + printfieldlist[printfieldcount] + "; ?>&emsp;&emsp;&emsp;\n"
                        else:   
                            str_form_input += "\t\t<?php echo $" + printfieldlist[printfieldcount] + "; ?><br><br>\n"
                    
                    
                    
                    #### closing bracket for button
                    str_form_input += "\t\t\t\t<?php\n\t\t\t}\n\n"
                
            ##### Closing php tag for all buttons which have printfields  
            str_form_input += "\t\t\t} \n\t\t?> \n" 
        
        ############################### handling input with no displayname ###################
        elif str_input_name == "" :
        
            #### handling input text , date , time
            if str_input_type == "text" or str_input_type == "date" or str_input_type == "time" or str_input_type == "password" or str_input_type == "checkbox":
                str_form_input += "\t\t" + str_input_start + str_input_type_print + str_input_id_print + str_input_name_print + str_input_placeholder_print + str_input_value + str_input_required + str_input_readonly + str_input_functiontype + str_input_end + str_input_newline + "\n"
            
            #### handling input radio
            elif str_input_type == "radio" :
                isfieldpresent = "no"
                for radiocount in range(0, len(parsed_masterjson['html']['form']['radio'])):
                    if parsed_masterjson['html']['form']['radio'][radiocount]['radiobuttons'][0]['name'] ==  str_input_id :
                        isfieldpresent = "yes"
                        for radiobuttoncount in range(0, len (parsed_masterjson['html']['form']['radio'][radiocount]['radiobuttons'])) :
                            str_radio_label = parsed_masterjson['html']['form']['radio'][radiocount]['radiobuttons'][radiobuttoncount]['label']
                            str_radio_value = " value = \"" + parsed_masterjson['html']['form']['radio'][radiocount]['radiobuttons'][radiobuttoncount]['value'] + "\" "
                            str_form_input += "\t\t" + str_input_start + str_input_type_print + str_input_id_print + str_radio_value + str_input_name_print + str_input_placeholder_print + str_input_value + str_input_required + str_input_readonly + str_input_functiontype + str_input_end + str_radio_label + str_tabspace
                    
                        str_form_input += str_input_newline + "\n"
                    
                if isfieldpresent == "no":
                    print "Input field " + str_input_display_name + " is not a valid radio field"
                    sys.exit("Input field " + str_input_display_name + " is not a valid radio field")
                
            
            #### handling input select
            elif str_input_type == "select" :
                isfieldpresent = "no"
                for selectcount in range(0,len(parsed_masterjson['html']['form']['select'])):
                    if parsed_masterjson['html']['form']['select'][selectcount]['selectid'] == str_input_id :
                        isfieldpresent = "yes"
                        str_form_input += "\t\t" + "<select "+ str_input_id_print + str_input_name_print + " >\n"
                        for optioncount in range(0, len (parsed_masterjson['html']['form']['select'][selectcount]['options'])):
                            str_select_item = parsed_masterjson['html']['form']['select'][selectcount]['options'][optioncount]['item']
                            str_select_value = parsed_masterjson['html']['form']['select'][selectcount]['options'][optioncount]['value']
                            str_form_input += "\t\t\t" + "<option value=\"" + str_select_value+ "\">" + str_select_item + " </option> \n"
                        str_form_input += "\t\t</select>" + str_input_newline + "\n"

                if isfieldpresent == "no":
                    print "Input field id " + str_input_id + " is not a valid select field"
                    sys.exit("Input field id " + str_input_id + " is not a valid select field")
                
            #### handling input textarea
            elif str_input_type == "textarea" :
                isfieldpresent = "no"
                for textareacount in range(0, len(parsed_masterjson['html']['form']['textarea'])) :
                    if str_input_id == parsed_masterjson['html']['form']['textarea'][textareacount]['name']:
                        isfieldpresent = "yes"
                        str_form_input += "\t\t" + "<textarea rows= \"" + parsed_masterjson['html']['form']['textarea'][textareacount]['rows'] + "\" cols= \"" + parsed_masterjson['html']['form']['textarea'][textareacount]['cols']+ "\" " + str_input_id_print + str_input_name_print + " >" + str_input_value.strip(" value = \" ") +  "</textarea> " + str_input_newline + "\n"
            
                if isfieldpresent == "no" :
                    print "Input field id " + str_input_id + " is not a valid textarea field"
                    sys.exit("Input field id " + str_input_id + " is not a valid textarea field")
            
            else:
                print "Input type " + str_input_type + " invalid"
                sys.exit("Input type " + str_input_type + " invalid")


        ######################### handling input with displayname (except plaintext) ############################
        else:
            #### handling input text, date, time
            if str_input_type == "text" or str_input_type == "date" or str_input_type == "time" or str_input_type == "password" or str_input_type == "checkbox" :
                str_form_input += "\t\t" + str_input_display_name_label + str_input_start + str_input_type_print + str_input_id_print + str_input_name_print + str_input_placeholder_print + str_input_value + str_input_required + str_input_readonly + str_input_functiontype + str_input_end + str_input_newline + "\n"
            
            #### handling input textarea
            elif str_input_type == "textarea":
                isfieldpresent = "no"
                for textareacount in range(0, len(parsed_masterjson['html']['form']['textarea'])) :
                    if str_input_display_name == parsed_masterjson['html']['form']['textarea'][textareacount]['displayname']:
                        isfieldpresent = "yes"
                        str_form_input += "\t\t" + str_input_display_name_label + "<textarea rows= \"" + parsed_masterjson['html']['form']['textarea'][textareacount]['rows'] + "\" cols= \"" + parsed_masterjson['html']['form']['textarea'][textareacount]['cols']+ "\" " + str_input_id_print + str_input_name_print + " >"+ str_input_value.strip(" value = \" ") +"</textarea> " + str_input_newline + "\n"
            
                if isfieldpresent == "no" :
                    print "Input field " + str_input_display_name + " is not a valid textarea field"
                    sys.exit("Input field " + str_input_display_name + " is not a valid textarea field")
                    
            #### handling input radio
            elif str_input_type == "radio":
                isfieldpresent = "no"
                for radiocount in range(0, len(parsed_masterjson['html']['form']['radio'])):
                    if parsed_masterjson['html']['form']['radio'][radiocount]['displayname'] ==  str_input_display_name :
                        isfieldpresent = "yes"
                        str_form_input += "\t\t" + str_input_display_name_label 
                        for radiobuttoncount in range(0, len (parsed_masterjson['html']['form']['radio'][radiocount]['radiobuttons'])) :
                            str_radio_label = parsed_masterjson['html']['form']['radio'][radiocount]['radiobuttons'][radiobuttoncount]['label']
                            str_radio_value = " value = \"" + parsed_masterjson['html']['form']['radio'][radiocount]['radiobuttons'][radiobuttoncount]['value'] + "\" "
                            str_form_input += str_input_start + str_input_type_print + str_input_id_print + str_radio_value + str_input_name_print + str_input_placeholder_print + str_input_value + str_input_required + str_input_readonly + str_input_functiontype + str_input_end + str_radio_label + str_tabspace
                    
                        str_form_input += str_input_newline + "\n"
                    
                if isfieldpresent == "no":
                    print "Input field " + str_input_display_name + " is not a valid radio field"
                    sys.exit("Input field " + str_input_display_name + " is not a valid radio field")
                    
            #### handling input select
            elif str_input_type == "select":
                isfieldpresent = "no"
                for selectcount in range(0,len(parsed_masterjson['html']['form']['select'])):
                    if parsed_masterjson['html']['form']['select'][selectcount]['selectid'] == str_input_id :
                        isfieldpresent = "yes"
                        str_form_input += "\t\t" + str_input_display_name_label + "\n\t\t" + "<select "+ str_input_id_print + str_input_name_print + " >\n"
                        for optioncount in range(0, len (parsed_masterjson['html']['form']['select'][selectcount]['options'])):
                            str_select_item = parsed_masterjson['html']['form']['select'][selectcount]['options'][optioncount]['item']
                            str_select_value = parsed_masterjson['html']['form']['select'][selectcount]['options'][optioncount]['value']
                            str_form_input += "\t\t\t" + "<option value=\"" + str_select_value+ "\">" + str_select_item + " </option> \n"
                        str_form_input += "\t\t</select>" + str_input_newline + "\n"

                if isfieldpresent == "no":
                    print "Input field id " + str_input_id + " is not a valid select field"
                    sys.exit("Input field id " + str_input_id + " is not a valid select field")
            
            else:  ############# Input type has typo error or is invalid, then throw error
                print "Input type " + str_input_type + " invalid"
                sys.exit("Input type " + str_input_type + " invalid")
                

    ######################### printing buttons (only html part of buttons)    ########################
    for buttoncount in range(0, len (parsed_json['html']['forms'][count]['button'])) :
        str_button_displayname = parsed_json['html']['forms'][count]['button'][buttoncount]['displayname'].strip()
        str_button_name = parsed_json['html']['forms'][count]['button'][buttoncount]['name'].strip()
        str_button_type = parsed_json['html']['forms'][count]['button'][buttoncount]['type'].strip()
        str_button_newline = parsed_json['html']['forms'][count]['button'][buttoncount]['newline'].strip()
        str_button_x_coordinate = parsed_json['html']['forms'][count]['button'][buttoncount]['x-coordinate'].strip()
        str_button_y_coordinate = parsed_json['html']['forms'][count]['button'][buttoncount]['y-coordinate'].strip()
        str_button_value = str_button_displayname
        str_html_button = "\t\t" + "<button type=\"" + str_button_type + "\" name=\"" + str_button_name + "\" value=\""+ str_button_value + "\" style=\"position:absolute; left: " + str_button_x_coordinate + "px; top:" + str_button_y_coordinate + "px;\">"+ str_button_displayname+ "</button> \n"
        
        ####adding button string to input string
        str_form_input += str_html_button   
    
    
    ################## adding php code for unprocessed buttons  ##############################
    
    for buttoncount in range(0, len (parsed_json['html']['forms'][count]['button'])) :
        str_button_displayname = parsed_json['html']['forms'][count]['button'][buttoncount]['displayname'].strip()
        str_button_name = parsed_json['html']['forms'][count]['button'][buttoncount]['name'].strip()
        str_button_type = parsed_json['html']['forms'][count]['button'][buttoncount]['type'].strip()
        str_button_newline = parsed_json['html']['forms'][count]['button'][buttoncount]['newline'].strip()
        str_button_x_coordinate = parsed_json['html']['forms'][count]['button'][buttoncount]['x-coordinate'].strip()
        str_button_y_coordinate = parsed_json['html']['forms'][count]['button'][buttoncount]['y-coordinate'].strip()
        str_button_value = str_button_displayname
            
        ###################  adding php code for button at top only if the button has not yet been processed  #######################################
        if str_button_displayname not in processed_buttons_list :
            ##handling button queries
            str_php_button = "\tif($_POST['submit']==\"" + str_button_value + "\") {\n"
            
            ###### iterating through query expression array
            for querycount in range(0, len (parsed_json['html']['forms'][count]['button'][buttoncount]['query'])) :
                querytype, variablelist, columnlist = splitquery(parsed_json['html']['forms'][count]['button'][buttoncount]['query'][querycount]['queryexpression'])
                
                for varlistcount in range(0, len(variablelist)) :
                    str_php_button += "\t\t$" + variablelist[varlistcount] + " = $_POST['" + variablelist[varlistcount] + "']; \n"
                    
                #for retaincount in range(0, len (parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'])) :
                    #str_php_button += "\t\t$_SESSION['" + parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'][retaincount]['fieldname'] + "'] = $" + parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'][retaincount]['fieldname'] + "; \n"

                
                str_php_button += "\t\t$sqlquery = \"" + parsed_json['html']['forms'][count]['button'][buttoncount]['query'][querycount]['queryexpression'] + "\"; \n"
                
                ####### if querytpe is insert or delete or update
                if querytype != "select":
                    str_php_button += "\t\tif(mysqli_query($db,$sqlquery)) { } \n"
                
                ####### if querytype is select then retrieve the column values from table
                else :
                    str_php_button += "\t\t$data = mysqli_query($db,$sqlquery); \n\t\twhile($row=mysqli_fetch_array($data)) { \n"
                    
                    for collistcount in range(0, len(columnlist)) :
                        str_php_button += "\t\t\t$" + columnlist[collistcount] + " = $row['" + columnlist[collistcount] + "']; \n"
                        
                    #######closing while
                    str_php_button += "\t\t}"
                #for retaincount in range(0, len (parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'])) :
                 #   str_php_button += "\t\t$_SESSION['" + parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'][retaincount]['fieldname'] + "'] = $" + parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'][retaincount]['fieldname'] + "; \n"

                for collistcount in range(0, len(columnlist)) :
                    for initializecount in range(0, len(parsed_json['php']['initialize'])):
                        if columnlist[collistcount] == parsed_json['php']['initialize'][initializecount]['name']:
                            str_php_button += "\t\t$_SESSION['" + columnlist[collistcount] + "'] = $" + columnlist[collistcount] + "; \n"
            
            for retaincount in range(0, len (parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'])) :
                str_php_button += "\t\t$_SESSION['" + parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'][retaincount]['fieldname'] + "'] = $" + parsed_json['html']['forms'][count]['button'][buttoncount]['retainfields'][retaincount]['fieldname'] + "; \n"
            str_php_button += "\n\t}"
            
        str_php += str_php_button
    
    
    ###### Closing validation function for current form and adding it to str_head_javascript
    str_head_validation += "\n}\n"
    str_head_javascript += str_head_validation

    
    str_form += str_form_input + "\n\t</form> \n "

###### close ajax function for all forms if it was created
if str_head_ajax != "" :    
    str_head_ajax += "});\n"

#print "validation fn list : " 
#print javascript_function_list
str_php += "\n\t}\n?>\n\n"  
str_head_ajax += "\n</script>\n</head>\n"  
str_file_total = str_php + str_head_javascript + str_head_ajax + str_html +str_form + "\n </body>" + "\n </html>"

out_file_name = parsed_json['program_name']   
	text_file = open(out_file_name, "w")
	text_file.write("%s" % str_file_total)
	print out_file_name
	text_file.close()

#text_fileht = open("C:\\xampp\\htdocs\\academicportal\\" + out_file_name, "w")
#text_fileht.write("%s" % str_file_total)
#text_fileht.close()

json_data.close();
masterjson_data.close();
