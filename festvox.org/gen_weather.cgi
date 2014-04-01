#!/usr/bin/perl
############################################################-*-mode:perl-*-
##                                                                       ##
##                   Carnegie Mellon University and                      ##
##                   Alan W Black and Kevin A. Lenzo                     ##
##                      Copyright (c) 1999-2000                          ##
##                        All Rights Reserved.                           ##
##                                                                       ##
##  Permission is hereby granted, free of charge, to use and distribute  ##
##  this software and its documentation without restriction, including   ##
##  without limitation the rights to use, copy, modify, merge, publish,  ##
##  distribute, sublicense, and/or sell copies of this work, and to      ##
##  permit persons to whom this work is furnished to do so, subject to   ##
##  the following conditions:                                            ##
##   1. The code must retain the above copyright notice, this list of    ##
##      conditions and the following disclaimer.                         ##
##   2. Any modifications must be clearly marked as such.                ##
##   3. Original authors' names are not deleted.                         ##
##   4. The authors' names are not used to endorse or promote products   ##
##      derived from this software without specific prior written        ##
##      permission.                                                      ##
##                                                                       ##
##  CARNEGIE MELLON UNIVERSITY AND THE CONTRIBUTORS TO THIS WORK         ##
##  DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING      ##
##  ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT   ##
##  SHALL CARNEGIE MELLON UNIVERSITY NOR THE CONTRIBUTORS BE LIABLE      ##
##  FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES    ##
##  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN   ##
##  AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,          ##
##  ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF       ##
##  THIS SOFTWARE.                                                       ##
##                                                                       ##
###########################################################################
# awb 03/04/00
# 
# Speak the current weather in the named state city
#

require "cgi-lib.pl";		# for forms
$ENV{'LIBWWW_PERL'}="/usr/local/lib/libwww-perl-0.40"; # for 'get'
 
$festvoxorg="/usr2/festvox/www.festvox.org";
$tmp="/tmp/weather_www".$$;
$festival=$festvoxorg."/bin/festival";
$ch_wave=$festvoxorg."/bin/ch_wave";
$logfile=$festvoxorg."/logs/gen_weather.log";
$weathercache=$festvoxorg."/ldom/weathercache/";
$weather_ldom_dir=$festvoxorg."/html/examples/cmu_weather_awb_ldom/";
$get_weather=$weather_ldom_dir."festvox/weather/bin/get_weather";

#---------------------------------------------------------------------------
$|=1;

open (MASTER, ">-"); # ">$master_file");

if (&ReadParse(*input)) {

    $state=$input{'state'};
    $city=$input{'city'};

    $state = lc($state);
    $state =~ s/[^a-z ]/ /g;
    $city = lc($city);
    $city =~ s/[^a-z ]/ /g;
    $ocity = $city;
    $ocity =~ s/ /_/g;
    $weatherwave=$weathercache.$state.".".$ocity.".wav";
    system($get_weather." \"".$state."\" \"".$city."\" >".$tmp.".out");

    if ( ! -e $weatherwave ) {
       system($festival." -b \"(voice_weather_ldom)\" \"(synth_weather \\\"".$tmp.".out\\\" \\\"".$weatherwave."\\\")\" >/tmp/wldom.out 2>&1");
   }

    # Do logging
    system("date >>".$logfile);
    open(LOG,">>".$logfile);
    print LOG $ENV{'REMOTE_ADDR'}."\n";
    print LOG $state."\n";
    print LOG $city."\n";
    open(FILE, "<".$tmp.".out");
    while (<FILE>) {
	print LOG $_;
    }
    close(FILE);
    print LOG "\n";
    close(LOG);

    # Return to the caller
      print MASTER "Content-type: audio/x-wav\n";
      print MASTER "\n";

      open(FILE, "<".$weatherwave);
      while (<FILE>) {
  	print MASTER $_;
      }
      close(FILE);

#      print MASTER "Content-type: text/plain\n";
#      print MASTER "\n";
#      print MASTER $state."\n";
#      print MASTER $city."\n";
#      print MASTER $weatherwave."\n";
#      print MASTER $get_weather." \"".$state."\" \"".$city."\" >".$tmp.".out";
#      print MASTER "\n";
#      open(FILE, "<".$tmp.".out");
#      while (<FILE>) {
#  	print MASTER $_;
#      }
#      close(FILE);
#      print MASTER "\n";
#      print MASTER "\n";
#      print MASTER $festival." -b \"(voice_weather_ldom)\" \"(synth_weather \\\"".$tmp.".out\\\" \\\"".$weatherwave."\\\")\""
    unlink($tmp.".out");

}
