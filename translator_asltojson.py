import json
import sys
import re
import os
from pprint import pprint
# **********************************************function for removing comments ************************************************#
def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurance streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("///.*?\n" ) ,"" ,string) # remove all occurance singleline comments (//COMMENT\n ) from string
    return string

# ********************************************** removing comments function END ***********************************************#

# ***************************************************processing inputs ********************************************************#
input_asl_file = [line.rstrip('\n') for line in open('input_asl_file.txt')]
asl_file=input_asl_file[0];

str_asl = open(asl_file, 'r').read()

str_asl = removeComments(str_asl)

# writing to a temp file.
with open(asl_file.rstrip(".txt") + "_temp.txt", "w") as text_file:
    text_file.write("%s" % str_asl)

#removing newlines and adding to a list..
with open(asl_file.rstrip(".txt") + "_temp.txt") as f_in:
    lines = (line.rstrip() for line in f_in) 
    lines = list(line for line in lines if line)
    
asl_file_content =lines

# removing the temporary file..
os.remove(asl_file.rstrip(".txt") + "_temp.txt")

# ***************************************************processing inputs ********************************************************#


 
str_json = "{\n"
str_tables = ""
str_php  = ""
str_javascript = "" 
str_ajax  = "" 
str_html = ""
str_links = ""
str_form = ""
str_button = ""

#------------------------------------START : Iterating through asl file content starts here-------------------------------------#


for aslfilecontentcount in range(0, len(asl_file_content)):
    
    if "apl_name :" in asl_file_content[aslfilecontentcount] or "apl_name:" in asl_file_content[aslfilecontentcount]:
    
        colonsplitlist = asl_file_content[aslfilecontentcount].split(":")
        
        str_json += "\"" + colonsplitlist[0].strip() + "\":\"" + colonsplitlist[1].strip() + "\",\n\n"
            
        
    
    if "program_name :" in asl_file_content[aslfilecontentcount] or "program_name:" in asl_file_content[aslfilecontentcount]:
    
        colonsplitlist = asl_file_content[aslfilecontentcount].split(":")
        
        str_json += "\"" + colonsplitlist[0].strip() + "\":\"" + colonsplitlist[1].strip() + "\",\n\n"
        
    
    if "tables :" in asl_file_content[aslfilecontentcount] or "tables:" in asl_file_content[aslfilecontentcount]:
        str_tables += "\"tables\" : [\n"
        aslfilecontentcount += 1
        
        while "php" not in asl_file_content[aslfilecontentcount]:
            #print "asl ***  " + asl_file_content[aslfilecontentcount]
            commasplitlist = asl_file_content[aslfilecontentcount].split(",")
            if len(commasplitlist) == 4 :
                str_tables += "\t{\"name\":\"" + commasplitlist[0].strip() + "\", \"alias\": \"" + commasplitlist[1].strip() + "\", \"read\": \"" + commasplitlist[2].strip() + "\", \"write\": \"" + commasplitlist[3].strip() + "\"},\n"

            aslfilecontentcount += 1
        str_tables = str_tables.strip("\n,")
        str_tables += "\n\n],\n\n"

    
    if "php :" in asl_file_content[aslfilecontentcount] or "php:" in asl_file_content[aslfilecontentcount]:
        str_php += "\"php\" : {\n"
        
        while "initialize" not in asl_file_content[aslfilecontentcount]:
            #print "asl ***  " + asl_file_content[aslfilecontentcount]
            aslfilecontentcount += 1
        str_php += "\"initialize\" : [\n"
        
        while not ("query:" in asl_file_content[aslfilecontentcount] or "query :" in asl_file_content[aslfilecontentcount] or "javascript:" in asl_file_content[aslfilecontentcount] or "javascript :" in asl_file_content[aslfilecontentcount] or "ajax :" in asl_file_content[aslfilecontentcount] or "ajax:" in asl_file_content[aslfilecontentcount] or "html:" in asl_file_content[aslfilecontentcount] or "html :" in asl_file_content[aslfilecontentcount]):
            #print "asl ***  " + asl_file_content[aslfilecontentcount]
            commasplitlist = asl_file_content[aslfilecontentcount].split(",")
            if len(commasplitlist) == 2 :
                str_php += "\t{\"name\":\"" + commasplitlist[0].strip() + "\", \"value\": \"" + commasplitlist[1].strip() + "\"},\n"

            aslfilecontentcount += 1
        str_php = str_php.strip("\n,")
        str_php += "\n\n],\n\n"
        
        str_php += "\"query\" : [\n"
        aslfilecontentcount +=1
        
        while not ("javascript:" in asl_file_content[aslfilecontentcount] or "javascript :" in asl_file_content[aslfilecontentcount] or "ajax :" in asl_file_content[aslfilecontentcount] or "ajax:" in asl_file_content[aslfilecontentcount] or "html:" in asl_file_content[aslfilecontentcount] or "html :" in asl_file_content[aslfilecontentcount]):
            query = asl_file_content[aslfilecontentcount]
            str_php += "\t\t\t{\"queryexpression\":\"" + query.strip() + "\"},\n"
            aslfilecontentcount +=1
        
        str_php = str_php.strip("\n,")
        str_php += "\n\n]\n\n"
        str_php +="},\n\n"
        
    # -----------------------------start processing javascript from here------------------------------ #
    
    if "javascript :" in asl_file_content[aslfilecontentcount] or "javascript:" in asl_file_content[aslfilecontentcount]:
        str_javascript += "\"javascript\" : {\n"
        aslfilecontentcount += 1
        
        ### processing javascript function till we don't encounter ajax
        while not("ajax :" in asl_file_content[aslfilecontentcount] or "ajax:" in asl_file_content[aslfilecontentcount] or "html:" in asl_file_content[aslfilecontentcount] or "html :" in asl_file_content[aslfilecontentcount]):
            ### process only if function is found
            if "function:"  in asl_file_content[aslfilecontentcount] or "function :" in asl_file_content[aslfilecontentcount]:
                aslfilecontentcount += 1
                str_javascript += "\"" + asl_file_content[aslfilecontentcount].strip() +"\" : {\n"  
                aslfilecontentcount += 1
                ### if source is self
                if "self" in asl_file_content[aslfilecontentcount]:
                    str_javascript += "\t\"source\" : \"self\",\n"
                    aslfilecontentcount += 1
                    str_javascript += "\t\"arguments\" : [\n"
                    aslfilecontentcount += 1
                    while "retrieved_fields" not in asl_file_content[aslfilecontentcount]:
                        commasplitlist = asl_file_content[aslfilecontentcount].split(",")
                        for arglength in range(0, len(commasplitlist)):
                            str_javascript += "\t\t{\"argname\":\"" + commasplitlist[arglength].strip() + "},\n"
                        aslfilecontentcount += 1
                    str_javascript = str_javascript.strip("\n,")

                    str_javascript += "\n\n],\n"
                    
                    str_javascript += "\t\"retrieved_fields\" : [\n"
                    aslfilecontentcount += 1
                    
                    while not("expressions :" in asl_file_content[aslfilecontentcount].strip(" \t ") or "expressions:" in asl_file_content[aslfilecontentcount].strip(" \t ")):
                        openangularsplitlist = asl_file_content[aslfilecontentcount].split("<")
                        openangularfirst = openangularsplitlist[0].split(",")
                        str_javascript += "\t\t{\"fieldname\":\" " + openangularfirst[0].strip() + "\", \"upperbound\": \"" + openangularfirst[1].strip() + "\", \"lowerbound\": \"" + openangularfirst[2].strip() +"\",\n"
                        
                        notallowedstrip = openangularsplitlist[1].strip(" > ")
                        notallowedlist = notallowedstrip.split(",")
                            
                        str_javascript += "\t\t\t\"notallowed\" : [\n"
                        for notallowedcount in range(0, len(notallowedlist)):
                            if notallowedlist[notallowedcount].strip(" >") =="" :
                                continue
                            str_javascript += "\t\t\t\t{\"value\":\" " + notallowedlist[notallowedcount].strip(" >") + "\"},\n"
                            
                        str_javascript = str_javascript.strip("\n,")
                        str_javascript += "\n\n\t\t\t\t],\n"
                        
                        mandatorystrip = openangularsplitlist[2].strip(" > ")
                        mandatorylist = mandatorystrip.split(",")
                            
                        str_javascript += "\t\t\t\"mandatory\" : [\n"
                        
                        for mandatorycount in range(0, len(mandatorylist)):
                            if mandatorylist[mandatorycount] == "":
                                continue
                            str_javascript += "\t\t\t\t{\"value\":\" " + mandatorylist[mandatorycount].strip() + "\"},\n"
                            
                        str_javascript = str_javascript.strip("\n,")
                        str_javascript += "\n\n\t\t\t\t]\n\t\t},\n\n"   
                        aslfilecontentcount += 1
                        
                    str_javascript = str_javascript.strip("\n,")
                    str_javascript += "\n\t\t],\n\n"
                    
                    if "expressions :" in asl_file_content[aslfilecontentcount] or "expressions:" in asl_file_content[aslfilecontentcount]:
                        str_javascript += "\t\"expressions\":[\n"
                        aslfilecontentcount += 1
                        while not("function :" in asl_file_content[aslfilecontentcount] or "function:" in asl_file_content[aslfilecontentcount]):
                            if "ajax :" in asl_file_content[aslfilecontentcount] or  "ajax:" in asl_file_content[aslfilecontentcount]or "html:" in asl_file_content[aslfilecontentcount] or "html:" in asl_file_content[aslfilecontentcount] or "html :" in asl_file_content[aslfilecontentcount]:
                                break;
                            commasplitlist = asl_file_content[aslfilecontentcount].split(",")
                            str_javascript += "\t\t{\"expression\":\"" + commasplitlist[0].strip() + "\", \"target_field\": \"" + commasplitlist[1].strip() + "\", \"default_value\": \"" + commasplitlist[2].strip() +"\"},\n"
                            aslfilecontentcount += 1
                        str_javascript = str_javascript.strip("\n,")
                        str_javascript += "\n\t\t]\n\t},\n"   
                    
                else:
                    str_javascript += "\"source\" : \"" +asl_file_content[aslfilecontentcount].strip() + "\"\n"
                    str_javascript = str_javascript.strip("\n,")
                    str_javascript += "\n},\n\n"
            
            else :
                if "ajax :" in asl_file_content[aslfilecontentcount] or  "ajax:" in asl_file_content[aslfilecontentcount]or "html:" in asl_file_content[aslfilecontentcount] or "html :" in asl_file_content[aslfilecontentcount]:
                    break;
                aslfilecontentcount +=1
            if "ajax :" in asl_file_content[aslfilecontentcount] or  "ajax:" in asl_file_content[aslfilecontentcount]or "html:" in asl_file_content[aslfilecontentcount] or "html :" in asl_file_content[aslfilecontentcount]:
                break    
            aslfilecontentcount +=1
        str_javascript = str_javascript.strip("\n,")
        str_javascript += "\n},\n\n"
        
    # -----------------------------start processing ajax from here------------------------------ #

    if "ajax :" in asl_file_content[aslfilecontentcount] or  "ajax:" in asl_file_content[aslfilecontentcount]:
        str_ajax +="\"ajax\":{\n"
        while not("html :" in asl_file_content[aslfilecontentcount] or  "html:" in asl_file_content[aslfilecontentcount]):
            if "function :" in asl_file_content[aslfilecontentcount] or  "function:" in asl_file_content[aslfilecontentcount]:
                aslfilecontentcount +=1
                str_ajax +="\t\""+ asl_file_content[aslfilecontentcount].strip() + "\":{\n\t\t\"retrieved_fields\":[\n"
                aslfilecontentcount +=2
                while not("method :" in asl_file_content[aslfilecontentcount] or  "method:" in asl_file_content[aslfilecontentcount]):
                    retfield = asl_file_content[aslfilecontentcount]
                    retcommasplit = retfield.split(",")
                    for retcount in range(0, len(retcommasplit)):
                        str_ajax += "\t\t\t{\"fieldname\":\"" + retcommasplit[retcount].strip() + "\"},\n"
                    aslfilecontentcount +=1
                str_ajax = str_ajax.strip( " \n,")    
                str_ajax += "\n\t\t],\n"
                aslfilecontentcount +=1
                while not("success :" in asl_file_content[aslfilecontentcount] or  "success:" in asl_file_content[aslfilecontentcount]):
                    methodlist = asl_file_content[aslfilecontentcount]
                    methodcommasplit = methodlist.split(",")
                    str_ajax += "\t\"type\":\""+ methodcommasplit[0].strip()+ "\",\n\t\"scriptfilename\":\""+ methodcommasplit[1].strip()+ "\",\n\t\"queryexpression\":\""+ methodcommasplit[2].strip() + "\",\n\t\"dataType\":\""+ methodcommasplit[3].strip() + "\",\n"
                    aslfilecontentcount +=1
                
                aslfilecontentcount +=1
                returntypelist = asl_file_content[aslfilecontentcount].split(",")
                str_ajax += "\t\"success\":{\n\t\t\"returndata\":\""+ returntypelist[0].strip() +  "\",\n\t\t\"delimiter\":\"" + returntypelist[1].strip() +  "\",\n\t\t\"outputlocations\":[\n"
                
                aslfilecontentcount +=2
                while not("html :" in asl_file_content[aslfilecontentcount] or  "html:" in asl_file_content[aslfilecontentcount]):
                    if "function :" in asl_file_content[aslfilecontentcount] or  "function:" in asl_file_content[aslfilecontentcount]:
                        break;
                    outfieldlist =  asl_file_content[aslfilecontentcount].split(",")
                    str_ajax += "\t\t\t{\"location\":\""+ outfieldlist[0].strip() + "\", \"type\": \""+ outfieldlist[1].strip()+ "\"},\n"
                    aslfilecontentcount +=1
                str_ajax = str_ajax.strip(" \n,")
                str_ajax += "\n\t\t\t]\n\t\t}\n"

                if "html :" in asl_file_content[aslfilecontentcount] or  "html:" in asl_file_content[aslfilecontentcount]:
                    str_ajax +="\n\t}\n"
                elif "function :" in asl_file_content[aslfilecontentcount] or  "function:" in asl_file_content[aslfilecontentcount]:
                    str_ajax +="\n\t},\n"
                else :
                    continue;
            else :
                if "html :" in asl_file_content[aslfilecontentcount] or  "html:" in asl_file_content[aslfilecontentcount]:
                    continue;
                else:
                    aslfilecontentcount +=1
        str_ajax +="\n},\n"
    
    # -----------------------------start processing html from here------------------------------
    if "html :" in asl_file_content[aslfilecontentcount] or  "html:" in asl_file_content[aslfilecontentcount]:
        str_html += "\"html\":{\n"
        aslfilecontentcount +=1
        #----------------------------links---------------------------------- raunak :  What if links are not present ?????
        
        if "links :" in asl_file_content[aslfilecontentcount] or  "links:" in asl_file_content[aslfilecontentcount]:
            aslfilecontentcount +=1
            str_links += "\t\"links\":[\n"
            while not("forms :" in asl_file_content[aslfilecontentcount] or  "forms:" in asl_file_content[aslfilecontentcount]):
                print asl_file_content[aslfilecontentcount]
                print "asl file count"
                print aslfilecontentcount
                linksplit = asl_file_content[aslfilecontentcount].split(",")
                print linksplit
                str_links += "\t\t{\"label\":\"" + linksplit[0].strip() + "\", \"target_page\":\"" + linksplit[1].strip() + "\", \"x-coordinate\":\""+ linksplit[2].strip() + "\", \"y-coordinate\":\""+ linksplit[3].strip() + "\" },\n"
                aslfilecontentcount +=1
            str_links = str_links.strip(" \n,") 
            str_links += "\n\t]," 


        if "forms :" in asl_file_content[aslfilecontentcount] or  "forms:" in asl_file_content[aslfilecontentcount]:
            print "inside forms"
            print asl_file_content[aslfilecontentcount]
            str_form +="\n\"forms\":[ \n"
            aslfilecontentcount +=1
            print "after forms:"
            print asl_file_content[aslfilecontentcount]
            if "form :" in asl_file_content[aslfilecontentcount] or  "form:" in asl_file_content[aslfilecontentcount]:
                while "form :" in asl_file_content[aslfilecontentcount] or  "form:" in asl_file_content[aslfilecontentcount]:
                    aslfilecontentcount +=1
                    formhead = asl_file_content[aslfilecontentcount].split(",")

                   
                    str_form += "\t{\n\t\"name\":\""+ formhead[0].strip() +"\",\n\t\"x-coordinate\":\""+ formhead[1].strip() + "\",\n\t\"y-coordinate\":\""+ formhead[2].strip() +"\",\n"
                    str_form += "\t\"class\":\""+ formhead[3].strip() + "\",\n\t\"method\":\""+ formhead[4].strip() +"\",\n\t\"action\":\""+ formhead[5].strip() + "\",\n"
                    str_form += "\t\"label\":\""+ formhead[6].strip() + "\",\n\t\"validation_function\":\""+ formhead[7].strip() + "\",\n\t\"layout\":\"" + formhead[8].strip() + "\",\n"

                    aslfilecontentcount +=1
                    #---------------------------input fields----------------------------------------------
                    if "form_input_fields :" in asl_file_content[aslfilecontentcount] or  "form_input_fields:" in asl_file_content[aslfilecontentcount]:
                        aslfilecontentcount +=1
                        str_form += "\n\t\"form_input_fields\":[\n"
                            
                        while not("buttons :" in asl_file_content[aslfilecontentcount] or  "buttons:" in asl_file_content[aslfilecontentcount] or "form :" in asl_file_content[aslfilecontentcount] or  "form:" in asl_file_content[aslfilecontentcount] or "END" in asl_file_content[aslfilecontentcount]):    
                            print "splitting"
                            print asl_file_content[aslfilecontentcount]
                            input_field = asl_file_content[aslfilecontentcount].split("<")
                            before_value = input_field[0].split(",")
                            angular_close = input_field[1].split(">")
                            value_list = angular_close[0]
                            after_value = angular_close[1].split(",")
                            str_form += "\t\t{\"name\":\""+ before_value[0].strip() + "\", \"id\":\"" + before_value[1].strip() + "\", \"type\":\"" + before_value[2].strip() +"\", \"placeholder\":\""+ before_value[3].strip() + "\", \"required\":\""+ before_value[4].strip() +"\","
                            str_form += "\"validation\":\""+ before_value[5].strip() + "\", \"newline\":\""+ before_value[6].strip() + "\", \"value\":\"" + value_list.strip() + "\" , \"readonly\":\""+ after_value[1].strip() + "\"," 
                            str_form += "\"fieldaction\":\"" + after_value[2].strip() + "\", \"functiontype\":\"" + after_value[3].strip() + "\", \"functionname\":\"" + after_value[4].strip() + "\" },\n"
                            aslfilecontentcount +=1
                        str_form = str_form.strip(" \n,")
                        str_form += "\n\t\t],"
        
                    #---------------------------buttons----------------------------------------------
                    if "buttons :" in asl_file_content[aslfilecontentcount] or  "buttons:" in asl_file_content[aslfilecontentcount]:
                        aslfilecontentcount +=1
                        str_button += "\n\t\"button\":[\n "

                        while "button_name :" in asl_file_content[aslfilecontentcount] or  "button_name:" in asl_file_content[aslfilecontentcount]:
                            aslfilecontentcount +=1
                            buttonhead = asl_file_content[aslfilecontentcount].split(",")

                            str_button += "\n\t{ \"displayname\": \""+ buttonhead[0].strip() + "\", \"type\":\"" + buttonhead[1].strip() + "\", \"name\":\"" + buttonhead[2].strip() + "\", \"x-coordinate\":\"" + buttonhead[3].strip() + "\","
                            str_button += "\"y-coordinate\":\""+ buttonhead[4].strip() +"\", \"newline\":\"" + buttonhead[5].strip() + "\",\n"                      
                            #retain fields
                            aslfilecontentcount +=2
                            str_button += "\n\"retainfields\":[\n"

                            while not("query :" in asl_file_content[aslfilecontentcount] or  "query:" in asl_file_content[aslfilecontentcount]):
                                retfield = asl_file_content[aslfilecontentcount]
                                retcommasplit = retfield.split(",")
                                for retcount in range(0, len(retcommasplit)):
                                    str_button += "\t\t\t{\"fieldname\":\"" + retcommasplit[retcount].strip() + "\"},\n"
                                aslfilecontentcount +=1
                            str_button = str_button.strip( " \n,")    
                            str_button += "\n\t\t],\n"
                                            
                            #query
                            aslfilecontentcount +=1
                            str_button += "\n\"query\":[\n"

                            while not("printfields :" in asl_file_content[aslfilecontentcount] or  "printfields:" in asl_file_content[aslfilecontentcount]):
                                query = asl_file_content[aslfilecontentcount]
                                str_button += "\t\t\t{\"queryexpression\":\"" + query.strip() + "\"},\n"
                                aslfilecontentcount +=1
                            
                            str_button = str_button.strip( " \n,")    
                            str_button += "\n\t\t],\n"
                            
                            #printfields
                            aslfilecontentcount +=1
                            str_button += "\n\"printfields\":[\n"
                            
                            while not("printhtmlfields :" in asl_file_content[aslfilecontentcount] or  "printhtmlfields:" in asl_file_content[aslfilecontentcount]):
                                printfield = asl_file_content[aslfilecontentcount]
                                printfieldcommasplit = printfield.split(",")
                                str_button += "\t\t\t{\"fieldname\":\"" + printfieldcommasplit[0].strip() + "\", \"newline\":\""+ printfieldcommasplit[1].strip() + "\", \"printposition\":\""+ printfieldcommasplit[2].strip() +"\"},\n"
                                aslfilecontentcount +=1
                            str_button = str_button.strip( " \n,")    
                            str_button += "\n\t\t],\n"
                            
                            #printhtml fields
                            aslfilecontentcount +=1
                            str_button += "\n\"printhtmlfields\":[\n"

                            while not("button_name :" in asl_file_content[aslfilecontentcount] or  "button_name:" in asl_file_content[aslfilecontentcount]):
                                if "form :" in asl_file_content[aslfilecontentcount] or  "form:" in asl_file_content[aslfilecontentcount] or "END" in asl_file_content[aslfilecontentcount]:
                                    break
                                
                                printhtmlfield = asl_file_content[aslfilecontentcount].split("<")
                                printhtmlfieldfirst = printhtmlfield[0]
                                printhtmlcommasplit = printhtmlfieldfirst.split(",")
                                printhtmlfieldsecond = printhtmlfield[1].split(">")
                                
                                printhtmlvalue = printhtmlfieldsecond[0]
                                
                                printhtmlthird = printhtmlfieldsecond[1].split(",")

                                str_button += "\t\t\t{\"fieldname\":\"" + printhtmlcommasplit[0].strip() + "\", \"printposition\":\"" + printhtmlcommasplit[1].strip() + "\" , \"name\":\""+  printhtmlcommasplit[2].strip()+ "\","
                                str_button += "\"type\":\""+ printhtmlcommasplit[3].strip() + "\", \"placeholder\":\"" + printhtmlcommasplit[4].strip() + "\", \"required\":\"" + printhtmlcommasplit[5].strip()+ "\", \"newline\":\"" + printhtmlcommasplit[6].strip()+ "\"," 
                                str_button += "\"value\":\"" + printhtmlvalue + "\"" 
                                str_button += ", \"readonly\":\"" + printhtmlthird[1].strip() + "\", \"fieldaction\":\"" + printhtmlthird[2].strip() + "\", \"functiontype\":\"" + printhtmlthird[3].strip() + "\", \"functionname\":\"" + printhtmlthird[4].strip() + "\"},\n"
                                aslfilecontentcount +=1
                            str_button = str_button.strip( " \n,")    
                            str_button += "\n\t\t]\n"
                        
                            #closing button tag for each button
                            if  "button_name :" in asl_file_content[aslfilecontentcount] or  "button_name:" in asl_file_content[aslfilecontentcount]:
                                str_button += "\t},\n"
                            else: 
                                str_button += "\t}\n"

                    #closing tag for all buttons array
                    str_button += "\n]},\n"

                    if "END" in asl_file_content[aslfilecontentcount]:
                        break;
                    if  "form :" in asl_file_content[aslfilecontentcount] or  "form:" in asl_file_content[aslfilecontentcount]:
                        continue;
                    else :
                        aslfilecontentcount +=1
            
            str_form += str_button       
            str_form = str_form.strip(" \n,")
            #closing tag for form array            
            str_form += "\n\t]" 

        else:
            aslfilecontentcount +=1

        str_html += str_links + str_form
        str_html += "\n\n\t}\n}" 
    # end condition of file end, final loop break.
    if "END" in asl_file_content[aslfilecontentcount]:
        print "END found!" 
        break;

#----------------------------------------------END : Iterating through asl file content ends here--------------------------------#


print str_json + str_tables + str_php + str_javascript + str_ajax + str_html
str_total = str_json + str_tables + str_php + str_javascript + str_ajax + str_html
text_file = open(asl_file.strip(".txt" ) + "_created.json" , "w")
text_file.write("%s" % str_total)
text_file.close()
