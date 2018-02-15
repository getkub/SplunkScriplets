#!/usr/bin/perl
# list all of the perl modules installed
use File::Find ;
for (@INC) { find(\&modules,$_) ; }
sub modules
{
        if (-d && /^[a-z]/) { $File::Find::prune = 1 ; return }
        return unless /\.pm$/ ;
        my $fullPath = "$File::Find::dir/$_";
        $fullPath =~ s!\.pm$!!;
        $fullPath =~ s#/(\w+)$#::$1# ;
        print "$fullPath \n";
}
