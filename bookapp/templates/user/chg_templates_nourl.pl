
use strict;

open(IN,"$ARGV[0]") or die "[error 1] $!\n";
##linux
system("cp -rf $ARGV[0] $ARGV[0].bk");
##cmd
#system("copy $ARGV[0] $ARGV[0]_bk")
open(OUT,">$ARGV[0].chg") or die "[error 2] $!\n";
print OUT "{% load static %}\n";

foreach my $l (<IN>){
	chomp($l);
	$l =~ s/\r//g;
	
	if($l =~ /link.*href="(.*?)"/){
		my $content = $1;
		my $new_content = "{% static '$content'%}";
		$l =~ s/$content/$new_content/;
	}
	elsif($l =~ /href="(.*?)\.html"/){
		my $content = $1;
		my $new_content = "#";
		$l =~ s/\.html//;
		$l =~ s/$content/$new_content/;
		
	}
	elsif($l =~ /script.*src="(.*?)"/){
		my $content = $1;
		my $new_content = "{% static '$content' %}";
		my $lt = $l;
		$l =~ s/$content/$new_content/;
	}
	elsif($l =~ /<img\s+src="(.*?)"/){
		my $content1 = $1;
		my $new_content1 = "{% static '$content1' %}";
		$l =~ s/$content1/$new_content1/;

	}
	elsif($l =~ /url\((.*?)\).*/){
		my $content1 = $1;
		my $new_content1 = "{% static '$content1' %}";
		$new_content1 =~ s/''/'/;
		$l =~ s/$content1/$new_content1/;

	}

	$l =~ s/\'\.\//\'/;

	print OUT "$l\n";
}

system("rm $ARGV[0]");
system("mv $ARGV[0].chg $ARGV[0]");
