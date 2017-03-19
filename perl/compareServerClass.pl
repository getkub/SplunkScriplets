#!/usr/bin/perl

# use strict;
# use warnings;


my $filename1 = 'compareInputList_EndPointServers.csv';
open(my $fh1, '<:encoding(UTF-8)', $filename1)
                or die "Could not open file '$filename1' $!";
chomp(my @hosts = <$fh1>);
close $filename1;

my $filename2 = '/tmp/my/serverclass.conf';
open(my $fh, '<:encoding(UTF-8)', $filename2)
                or die "Could not open file '$filename2' $!";
chomp(my @myServerClass = <$fh>);
close $filename2;

 @server_class = (@myServerClass, @admin);


foreach(@hosts) {
                $host = $_;
                # chomp $host;
                # print "Host = $host\n";
                @values = split(',', $host);
                $host = $values[0];
                print "Host = $host\n";
                foreach(@server_class) {
                                $row = $_;
                                # chomp $row;
                                # print "$row\n";

                                if (substr($row, 0 ,1) eq '[' )
                                {
                                                # print "Stanza: $row \n";
                                                $stanza = $row;
                                }
                                if ( (substr($row, 0 ,5) eq 'white' ) ||
                                                (substr($row, 0 ,5) eq 'black' ) )
                                {
                                                @values = split('=', $row);
                                                $reg = $values[1];
                                                $reg =~ s/^\s+|\s+$//g;
                                                $reg =~ s/\*/\.\*/g;

                                                if ( $reg eq "")
                                                {
                                                                next;
                                                }

                                                $regex = qr/$reg/;

                                                if ($host =~ /$reg/)
                                                {
                                                                # print "Regex: " . $reg . "\n";
                                                                # print "Row: " . $row . "\n";
                                                                print "MATCHED: " . $host . " = " . $values[0] . ":"  . $reg . " = " . $stanza . "\n";
                                                                # exit;
                                                }

                                }
                }
                print "=============\n";
                # exit;
}
