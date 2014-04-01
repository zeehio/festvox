#!/usr/local/bin/perl

# Perl Routines to Manipulate CGI input
#
# Copyright (c) 1995 Steven E. Brenner
# Permission granted to use and modify this library so long as the
# copyright above is maintained, modifications are documented, and
# credit is given for any use of the library.
#
# Thanks are due to many people for reporting bugs and suggestions
# especially Meng Weng Wong, Maki Watanabe, Bo Frese Rasmussen,
# Andrew Dalke, Mark-Jason Dominus, Dave Dittrich, Jason Mathews

# For more information, see:
#     http://www.bio.cam.ac.uk/web/form.html
#     http://www.seas.upenn.edu/~mengwong/forms/

# Minimalist http form and script (http://www.bio.cam.ac.uk/web/minimal.cgi):
#
# require "cgi-lib.pl";
# if (&ReadParse(*input)) {
#    print &PrintHeader, &PrintVariables(%input);
# } else {
#   print &PrintHeader,'<form><input type="submit"> Data: <input name="myfield">';
#}

# ReadParse
# Reads in GET or POST data, converts it to unescaped text,
# creates key/value pairs in %in, using '\0' to separate multiple
# selections

# Returns TRUE if there was input, FALSE if there was no input
# UNDEF may be used in the future to indicate some failure.

# Now that cgi scripts can be put in the normal file space, it is useful
# to combine both the form and the script in one place.  If no parameters
# are given (i.e., ReadParse returns FALSE), then a form could be output.

# If a variable-glob parameter (e.g., *cgi_input) is passed to ReadParse,
# information is stored there, rather than in $in, @in, and %in.

sub ReadParse {
  local (*in) = @_ if @_;
  local ($i, $key, $val);

  # Read in text
  if (&MethGet) {
    $in = $ENV{'QUERY_STRING'};
  } elsif (&MethPost) {
    read(STDIN,$in,$ENV{'CONTENT_LENGTH'});
  }

  @in = split(/[&;]/,$in);

  foreach $i (0 .. $#in) {
    # Convert plus's to spaces
    $in[$i] =~ s/\+/ /g;

    # Split into key and value.
    ($key, $val) = split(/=/,$in[$i],2); # splits on the first =.

    # Convert %XX from hex numbers to alphanumeric
    $key =~ s/%(..)/pack("c",hex($1))/ge;
    $val =~ s/%(..)/pack("c",hex($1))/ge;

    # Associate key and value
    $in{$key} .= "\0" if (defined($in{$key})); # \0 is the multiple separator
    $in{$key} .= $val;

  }

  return scalar(@in);
}


# PrintHeader
# Returns the magic line which tells WWW that we're an HTML document

sub PrintHeader {
  return "Content-type: text/html\n\n";
}


# HtmlTop
# Returns the <head> of a document and the beginning of the body
# with the title and a body <h1> header as specified by the parameter

sub HtmlTop
{
  local ($title) = @_;

  return <<END_OF_TEXT;
<html>
<head>
<title>$title</title>
</head>
<body>
<h1>$title</h1>
END_OF_TEXT
}

# Html Bot
# Returns the </body>, </html> codes for the bottom of every HTML page

sub HtmlBot
{
   return "</body>\n</html>\n";
 }


# MethGet
# Return true if this cgi call was using the GET request, false otherwise

sub MethGet {
  return ($ENV{'REQUEST_METHOD'} eq "GET");
}


# MethPost
# Return true if this cgi call was using the POST request, false otherwise

sub MethPost {
  return ($ENV{'REQUEST_METHOD'} eq "POST");
}


# MyURL
# Returns a URL to the script

sub MyURL  {
  local ($port);
  $port = ":" . $ENV{'SERVER_PORT'} if  $ENV{'SERVER_PORT'} != 80;
  return  'http://' . $ENV{'SERVER_NAME'} .  $port . $ENV{'SCRIPT_NAME'};
}


# CgiError
# Prints out an error message which which containes appropriate headers,
# markup, etcetera.
# Parameters:
#  If no parameters, gives a generic error message
#  Otherwise, the first parameter will be the title and the rest will
#  be given as different paragraphs of the body

sub CgiError {
  local (@msg) = @_;
  local ($i,$name);

  if (!@msg) {
    $name = &MyURL;
    @msg = ("Error: script $name encountered fatal error");
  };

  print &PrintHeader;
  print "<html><head><title>$msg[0]</title></head>\n";
  print "<body><h1>$msg[0]</h1>\n";
  foreach $i (1 .. $#msg) {
    print "<p>$msg[$i]</p>\n";
  }
  print "</body></html>\n";
}


# CgiDie
# Identical to CgiError, but also quits with the passed error message.

sub CgiDie {
  local (@msg) = @_;
  &CgiError (@msg);
  die @msg;
}


# PrintVariables
# Nicely formats variables in an associative array passed as a parameter
# And returns the HTML string.
sub PrintVariables {
  local (%in) = @_;
  local ($old, $out, $output);
  $old = $*;  $* =1;
  $output .=  "\n<dl compact>\n";
  foreach $key (sort keys(%in)) {
    foreach (split("\0", $in{$key})) {
      ($out = $_) =~ s/\n/<br>\n/g;
      $output .=  "<dt><b>$key</b>\n <dd><i>$out</i><br>\n";
    }
  }
  $output .=  "</dl>\n";
  $* = $old;

  return $output;
}

# PrintVariablesShort
# Now obsolete; just calls PrintVariables

sub PrintVariablesShort {
  return &PrintVariables(@_);
}

1; #return true


