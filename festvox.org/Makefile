###########################################################################
##                                                                       ##
##                   Carnegie Mellon University and                      ##
##                   Alan W Black and Kevin A. Lenzo                     ##
##                      Copyright (c) 1998-2000                          ##
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
##                                                                       ##
##  The festvox.org html pages                                           ##
##                                                                       ##
##  These aren't put in the festvox distribution but are included in     ##
##  the CVS tree and in backups                                          ##
##                                                                       ##
###########################################################################
TOP=..
DIRNAME=festvox.org
BUILD_DIRS = ldom dbs festival cmu_arctic cmu_faf cmu_sin \
             blizzard transform
ALL_DIRS = images $(BUILD_DIRS)
HTMLBITS=header.html sidebar.html footer.html body.html
HTMLBODIES=index_body.html contact_body.html links_body.html \
           download_body.html voicedemos_body.html \
           exampledbs_body.html maillists_body.html search_body.html \
	   search_results_body.html contrib_body.html festcourse_body.html
FINALHTML= $(HTMLBODIES:_body.html=.html)
PERL= cgi-lib.pl gen_fest.cgi gen_time_ldom.cgi gen_time_ldom_npt.cgi \
      search searchindex gen_weather.cgi
OTHERS = make_html festvox-talk.info
FILES = Makefile $(HTMLBITS) $(HTMLBODIES) $(PERL) $(OTHERS) klatt.html

ALL = $(FINALHTML) default-results.txt

LOCAL_CLEAN = $(FINALHTML) *.tmp.html default-results.txt

include $(TOP)/config/common_make_rules

%.html : %_body.html $(HTMLBITS) make_html
	@ ./make_html $< "" header.html footer.html sidebar.html >$@

default-results.txt: search_results.html
	@ sed 's+src="+src="/+' search_results.html | \
	  sed 's+href="+href="/+' | \
	  sed 's+href="/http+href="http+' | \
	  sed 's+href="/http+href="http+' | \
          sed 's/Festvox: /Festvox: Search Results/' > default-results.txt

install:
ifdef BUILD_DIRS
	@ for i in $(BUILD_DIRS) ; \
	do \
	   $(MAKE) -C $$i --no-print-directory install; \
	done
endif
	scp -p $(FINALHTML) token2.metronomicon.com:websites/www.festvox.org/html
#	scp -p $(PERL) token.metronomicon.com:websites/www.festvox.org/cgi-bin
	scp -p default-results.txt token2.metronomicon.com:websites/www.festvox.org/cgi-bin/searchdata/templates/default-results.txt

# Becuase so many browsers only look at the file extension we install
# the cgi scripts with names ending in .wav 
install-cgi:
	scp -p gen_time_ldom_npt.cgi token2.metronomicon.com:websites/festvox.org/cgi-bin/gen_time2_ldom_npt.wav
	scp -p gen_time_ldom.cgi token2.metronomicon.com:websites/festvox.org/cgi-bin/gen_time2_ldom.wav
	scp -p gen_fest.cgi token2.metronomicon.com:websites/festvox.org/cgi-bin/gen_fest.wav
	scp -p gen_weather.cgi token2.metronomicon.com:websites/festvox.org/cgi-bin/gen_weather.wav


