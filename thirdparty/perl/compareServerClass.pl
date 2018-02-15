#!/usr/bin/perl

# use strict;
# use warnings;

# ============================================== #
# Script to verify if a list of clients are present in multiple serverclass
# Outputs the stanza for whitelist/blacklist
# tags: validate Serverclass, check Serverclass
# ============================================== #


my $filename1 = 'clients.list';
open(my $fh1, '<:encoding(UTF-8)', $filename1)
                or die "Could not open file '$filename1' $!";
chomp(my @hosts = <$fh1>);
close $filename1;

my $filename2 = 'listofServerClass.list';
open(my $fh, '<:encoding(UTF-8)', $filename2)
                or die "Could not open file '$filename2' $!";
chomp(my @serverClassList = <$fh>);
close $filename2;


# print join("\n", @serverClassList);
# @server_class = (@myServerClass, @admin);


foreach(@hosts) {
                $host = $_;
                # chomp $host;
                # print "Host = $host\n";
                @values = split(',', $host);
                $host = $values[0];
                print "Host = $host\n";
                foreach $item (@serverClassList) {
                    open(my $fh2, '<:encoding(UTF-8)', $item)
                        or do {
                                warn "WARN: Could not open file '$item' $!";
                            };
                    chomp(my @server_class = <$fh2>);
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
                                                                    print "MATCHED: " . $host . " = " . $values[0] . ":"  . $reg . " = " . $stanza . " file=" . $item . "\n";
                                                                    # exit;
                                                    }
    
                                    }
                    }
                    close $item;
                }
                print "=============\n";
                # exit;
}
