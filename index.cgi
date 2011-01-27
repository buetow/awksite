#!/usr/bin/awk -f
#
# AWKsite v0.2
#
# AWK CGI website main program file
#
# AWK CGI is Copyright by Paul C. Buetow (2005)
#	http://buetow.org 
#	Runs on FreeBSD 6.x 
#
# AWK CGI is Copyright by Paul C. Buetow (2009)
#	Update for Debian Lenny (GNU AWK)
#

BEGIN {
  config_file = "awksite.conf"

  read_config_values(config_file)
  print_http_header()
  process_foreach_line()
}

function print_http_header() {
  print "Content-type: text/html\n\n"
}

function read_config_values(config_file) {
  while ((getline < config_file) > 0) {
    position = index($0,"=")
    if (position == 0 || /^#/)
      continue

    key = substr($0, 0, position)
    val = substr($0, position+1, 100)

    if (val ~ /^!/) 
       substr(val, 2, 100) | getline val	

    values[key] = val
  }

  close(config_file)
}

function process_foreach_line() {
  template_file = values["template"]

  while ((getline < template_file) > 0)
    print process_line($0)
  close(template_file)
}

function process_line(line) {
  if (line ~ /%%.+%%/)
    return insert_template_value(line) 
  return line
}

function insert_template_value(line) {
   position1 = index(line, "%%") + 2 
   temp = substr(line, position1, 100)

   if ((position2 = index(temp, "%%") ) == 1 ) 
	return line

   key = substr(temp, 0, position2)  

   if (key ~ /^!sort /) 
     values[key] = read_file_sorted(substr(key, 7, 100))

   gsub("%%" key "%%", values[key], line)

   if (line ~ /%%/) 
	return insert_template_value(line)

   return line 
}

function read_file_sorted(file) {
   retval = ""; command = "cat " file " | sort"
   while (( command | getline ) > 0 )
     retval = retval $0 "<br>\n"
   return retval
}

function debug(message) {
   print "DEBUG " message
}
