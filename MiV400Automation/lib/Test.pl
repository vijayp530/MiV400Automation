#!C:/Strawberry/perl/bin
#!C:/Dwimperl/perl/bin
#use strict;
use warnings;
# Create a user agent object
use LWP::UserAgent;
use LWP::ConnCache;
use HTTP::Request::Common;
use File::Slurp;
#use XML::LibXML;
#use XML::LibXML;
#use LWP::UserAgent;
#use LWP::ConnCache;
use 5.14.2;
#$| =1;
#print "Start Perl \n";
my $file_name =$ARGV[0];
my $ip_add =  $ARGV[1];
my $file_content = $file_name;
#my $file_content = $file_name;
my $add_header = 'xml=';
$file_content = $add_header.$file_content;

# file_content = xml=xml entries passed
#print "FILE CONTENT IN PERL: ";
#print $file_content;
#print "\n";

my $ip_header = 'http://';
$ip_add = $ip_header.$ip_add;

# ip_add = http://10.112.95.160

#print "\nIP ADDR IN PERL:";
#print $ip_add;

my $ua = LWP::UserAgent->new(agent => 'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)');
$ua->conn_cache(LWP::ConnCache->new());
my $resp = $ua->request(
                POST $ip_add ,
                Content_Type => 'application/x-www-form-urlencoded',
                Content      => $file_content);
