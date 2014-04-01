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
# awb 04/02/00
# CGI script for general festival synthesis using festival as a server
# (but awb doesn't know any perl ...)

require "cgi-lib.pl";		# for forms
$ENV{'LIBWWW_PERL'}="/usr/local/lib/libwww-perl-0.40"; # for 'get'
 
$festvoxorg="/usr2/festvox/www.festvox.org";
# modified by duncan to fix /tmp overflowing 1/5/2002
$tmp="/tmp2/tts_www".$$;
#$tmp="/tmp/tts_www";
$text2wave=$festvoxorg."/bin/text2wave";
$ch_wave=$festvoxorg."/bin/ch_wave";
$logfile=$festvoxorg."/logs/gen_fest.log";

#---------------------------------------------------------------------------
$|=1;

open (MASTER, ">-"); # ">$master_file");

if (&ReadParse(*input)) {

    $format=$input{'format'};
    $voice=$input{'voice'};
    $text=$input{'text'};

    $festvoice="voice_kal_diphone";  # default voice
    if ($voice eq "kal (American Male)")
    {
	$festvoice="voice_kal_diphone";
    }
    if ($voice eq "rab (British Male)")
    {
	$festvoice="voice_rab_diphone";
    }
    if ($voice eq "ked (American Male)") 
    {
	$festvoice="voice_ked_diphone";
    }
    if ($voice eq "bdl_arctic_hts (American Male)") 
    {
	$festvoice="voice_cmu_us_bdl_arctic_hts";
    }
    if ($voice eq "slt_arctic_hts (American Female)") 
    {
	$festvoice="voice_cmu_us_slt_arctic_hts";
    }
    if ($voice eq "jmk_arctic_hts (American Male)") 
    {
	$festvoice="voice_cmu_us_jmk_arctic_hts";
    }
    if ($voice eq "awb_arctic_hts (Scottish Male)") 
    {
	$festvoice="voice_cmu_us_awb_arctic_hts";
    }
    if ($voice eq "us1 (American Female, MBROLA)") 
    {
	$festvoice="voice_us1_mbrola";
    }
    if ($voice eq "us2 (American Male, MBROLA)") 
    {
	$festvoice="voice_us2_mbrola";
    }
    if ($voice eq "us3 (American Male, MBROLA)") 
    {
	$festvoice="voice_us3_mbrola";
    }
    if ($voice eq "don (British Male)") 
    {
	$festvoice="voice_don_diphone";
    }
    if ($voice eq "el (Spanish Male)") 
    {
 	$festvoice="voice_el_diphone";
    }

    $festformat="riff";
    
    open(TXT,">".$tmp.".text");
    print TXT $text;
    close(TXT);

    system($text2wave." -eval \"(".$festvoice.")\" -o ".$tmp.".wav -otype ".$festformat." ".$tmp.".text >$tmp.out 2>&1");

    # Do logging
    system("date >>".$logfile);
    open(LOG,">>".$logfile);
    print LOG $ENV{'REMOTE_ADDR'}."\n";
    print LOG $festvoice."\n";
    print LOG $text."\n";
    print LOG "\n";
    close(LOG);

    # Return to the caller
    if ($format eq "wav")
    {
  	print MASTER "Content-type: audio/x-wav\n";
  	print MASTER "\n";
    }
    if ($format eq "aiff")
    {
	print MASTER "Content-type: audio/x-aiff\n";
 	print MASTER "\n";
 	system($ch_wave." -otype aiff -o ".$tmp.".wav ".$tmp.".wav");
    }
    if ($format eq "sun")
    {
	print MASTER "Content-type: audio/x-sun\n";
	print MASTER "\n";
	system($ch_wave." -otype snd -o ".$tmp.".wav ".$tmp.".wav");
    }
    if ($format eq "ulaw")
    {
	print MASTER "Content-type: audio/basic\n";
	print MASTER "\n";
        # actually we put a sun header on it
	system($ch_wave." -otype snd -ostype mulaw -F 8000 -o ".$tmp.".wav ".$tmp.".wav");
    }

    # I wonder if this really is the best way to cat a binary file
    open(FILE, "<".$tmp.".wav");
    while (<FILE>) {
	print MASTER $_;
    }
    close(FILE);

#    print MASTER "Content-type: text/plain\n";
#    print MASTER "\n";
#    print MASTER $format."\n";
#    print MASTER $voice."\n";
#    print MASTER $text."\n";
#    print MASTER $festvoice."\n";
#    print MASTER $text2wave." -eval \"(".$festvoice.")\" -o ".$tmp.".wav -otype ".$festformat." ".$tmp.".text\n";

    unlink($tmp.".text");
    unlink($tmp.".comms");
    unlink($tmp.".wav");
    unlink($tmp.".out");

}
