#!/usr/bin/perl
###########################################################################
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
# awb 06/02/00
# 
# Speak the current time
#

require "cgi-lib.pl";		# for forms
$ENV{'LIBWWW_PERL'}="/usr/local/lib/libwww-perl-0.40"; # for 'get'
 
$festvoxorg="/usr2/festvox/www.festvox.org";
$tmp="/tmp/tts_www".$$;
#$tmp="/tmp/tts_www";
$text2wave=$festvoxorg."/bin/text2wave";
$festival=$festvoxorg."/bin/festival";
$ch_wave=$festvoxorg."/bin/ch_wave";
$logfile=$festvoxorg."/logs/gen_time_ldom.log";

#---------------------------------------------------------------------------
$|=1;

open (MASTER, ">-"); # ">$master_file");

if (&ReadParse(*input)) {

    $voice=$input{'voice'};

    open(FEST,"| $festival >/dev/null 2>&1");
    $festvoice="voice_time_ldom";  # default voice
    if ($voice eq "normal")
    {
	$festvoice="voice_time_ldom";
    }
    if ($voice eq "trent")
    {
	$festvoice="voice_ttime_ldom";
    }
    if ($voice eq "golem")
    {
	$festvoice="voice_gtime_ldom";
    }
    if ($voice eq "kalawb")
    {
	$festvoice="voice_cmu_time_ka_ldom";
    }
    if ($voice eq "hemos")
    {
	$festvoice="voice_cepstral_time_hemos_ldom";
    }
    if ($voice eq "falsetto")
    {
	$festvoice="voice_ftime_ldom";
    }
    if ($voice eq "chinese")
    {
	$festvoice="voice_chtime_ldom";
    }
    if ($voice eq "nepali")
    {
	$festvoice="voice_cmu_time_srm_ldom";
    }
    if ($voice eq "japanese")
    {
	$festvoice="voice_cmu_jtime_ftm_ldom";
    }
    print FEST "(".$festvoice.")\n";
    print FEST "(savetime \"".$tmp.".wav\")\n";
    close(FEST);

    # Do logging
    system("date >>".$logfile);
    open(LOG,">>".$logfile);
    print LOG $ENV{'REMOTE_ADDR'}."\n";
    print LOG $festvoice."\n";
    print LOG "\n";
    close(LOG);

    # Return to the caller
    print MASTER "Content-type: audio/x-wav\n";
    print MASTER "\n";

    open(FILE, "<".$tmp.".wav");
    while (defined ($x=<FILE>)) {
	print MASTER $x;
    }
    close(FILE);

#    print MASTER "Content-type: text/plain\n";
#    print MASTER "\n";
#    print MASTER $festvoice."\n";

    unlink($tmp.".wav");

}
