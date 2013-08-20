#!/usr/bin/perl -w
use strict;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

print "Content-Type: text/html\n\n";
print <<HTML;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
<title>AddComment</title>
<style>
	div{margin-bottom: 5px; padding-left: 10px;}
</style>
</head>
<body>
<a href="01_index.cgi"><h1>add your coments</h1></a>
HTML

print "<a href='#bottom' name='top'><p>Go bottom</p></a>";

my $query = CGI->new();
my $name;
my $text;
my @error;

if($query->param('name')){
	if( $query->param('name') =~ /^[a-zA-Z0-9]{4,16}$/ ) { $name = $query->param('name') }
	else { push @error, "Field Name can contain 4-16 only alphanummeric simbols" }
}
#else { push @error, "Enter your name" }
if($query->param('text')){
	if( $query->param('text') =~ /\<[\w\\]/i ) { push @error, "Field Text can't contain tags (<...>)" }
	else { $text = $query->param('text') }
}
#else { push @error, "Enter your comments" }
if(!@error){
	if($name && !$text) { push @error, "Enter your comments" }
	if(!$name && $text) { push @error, "Enter your name" }
}

if( $name && $text && !@error ){
	eval { myDBfunc::send_data("task61", $name, $text) };
	if ($@) { push @error, "Problem with sending your message: $@\n" } 
	else { 
		eval { $query->redirect('01_index.cgi') };
		if($@){push @error, "Problem with reloading page: $@\n"};
	}	
}

print <<HTML;
<form method="POST">
	<label for="name">Enter your name:</label>
	<input name="name" type="text" size="30" value="$name" placeholder="Name"><br/><br/>
	<label for="text">Enter your comment:</label>
	<textarea name="text" cols="30" rows="10" value="$text" placeholder="Text"></textarea><br/><br/>
	<input type="submit" value="Send your comment" id="submit">
</form>
HTML
if(@error){
	print "<div style='background: pink; border: solid red 1px;'>";
	foreach my $error (@error){print "<p>$error</p>"};
	print "</div>";
}

my $answer;
eval { $answer = myDBfunc::get_data("task61") };
if ($@) { push @error, "Error happened: $@\n" }
else { 
	foreach my $string (reverse @$answer){
		print "<div style='background: #e0e0e0; border: solid green 1px;'>";
		my $idid = $$string[0];
		my $name = $$string[1];
		my $text = $$string[2];
		$text =~ s/\n/<br\/>/g;
		my $time = $$string[3];
		print "<h5>$name</h5>";
		print "<p><em>id: $idid, date: $time</em></p>";
		print "<p>$text</p>";
		print "</div>";
	}
};

print "<a href='#top' name='bottom'><p>Go top</p></a>";
print "</body>\n</html>\n";


package myDBfunc;
use DBI;

sub connect_to_db{
	my $host = "localhost";
	my $port = "3306";
	my $db =  shift;
	my $user = "test";
	my $password = "123qwe123";
	my $dsn = "DBI:mysql:database=$db;host=$host;port=$port";
	my $dbh;
	eval { $dbh = DBI->connect($dsn, $user, $password, { RaiseError => 1, PrintError => 0 } ) };
	if($@){print STDERR "Unable to connect:\n$@"; return 0} #$DBI::errstr

	if ($dbh->ping) { return $dbh } else { return 0 }
};

sub get_data{
	my $ans;
	my $dbh = connect_to_db(shift);
	eval {
		my $sth = $dbh->prepare('SELECT * FROM coments');
		$sth->execute();
		$ans = $sth->fetchall_arrayref;
		$sth->finish;
	};
	$dbh->disconnect;
	if ($@) { print STDERR "Error happened: $@\n"; return 0 } else { return $ans }
};

sub send_data{
	my $dbh = connect_to_db(shift);
	my $name = shift;
	my $text = shift;
	eval {
		my $sth = $dbh->prepare('INSERT INTO coments (username,coment) VALUES (?,?)');
		$sth->execute($name, $text);#, $time);
		$sth->finish;
	};
	if ($@) { print STDERR "Error happened: $@\n"; return 0 } else { return 1 }
}
1;