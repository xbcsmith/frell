#!/usr/bin/perl
#
use strict;
use warnings;
#
use LWP::Simple;
#
print "Url  : $ARGV[1]\n";
print "File : $ARGV[2]\n";

my $url = $ARGV[1];
my $file = $ARGV[2];
#
getstore($url, $file);
