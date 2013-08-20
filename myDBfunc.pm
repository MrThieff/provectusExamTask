#!/usr/bin/perl -w
package myDBfunc;
#use Exporter qw(import);
#use vars qw(@ISA @EXPORT);

BEGIN {
	use DBI;
	use Exporter();
	@ISA = 'Exporter';
	@EXPORT = qw(
		&get_data
		&connect_to_db
		&send_new_quote
		&get_new_quote
		&create_uid
	);
};

sub connect_to_db{
	my $host = "localhost";
	my $port = "3306";
	my $db =  shift;
	my $user = "test";
	my $password = "123qwe123";
	my $dsn = "DBI:mysql:database=$db;host=$host;port=$port;";
	my $dbh;
	eval { $dbh = DBI->connect($dsn, $user, $password, { RaiseError => 1, PrintError => 0 } ); $dbh->do("SET NAMES 'utf8'"); };
	if($@){ return "Unable to connect: $@\n" } #$DBI::errstr
	else { if ($dbh->ping) { return $dbh } else { return "Unable to connect: ping error.\n" }; };
};

sub get_data{
	my $ans;
	my $dbh;
	eval { $dbh = connect_to_db(shift); };
	if ($@) { return "Connection error: $dbh\n" };
	my $queryString = shift;
	eval {
		my $sth = $dbh->prepare($queryString);
		$sth->execute();
		$ans = $sth->fetchall_arrayref;
		$sth->finish;
	};
	$dbh->disconnect;
	if ($@) { return "Error happened: $@\n" } else { return $ans }
};

sub send_new_quote{
	my $ans;
	my $dbh;
	eval { $dbh = connect_to_db(shift); };
	if ($@) { return "Connection error: $dbh\n" };
	my $quotes = shift;
	my @error;
	if(@$quotes){
		my $error;
		my $queryString = "INSERT INTO bash (id, quote) VALUES (?, ?);";
		my $sth = $dbh->prepare($queryString);
		foreach my $quote (@$quotes){
			eval {$sth->execute($$quote{'id'}, $$quote{'quote'}) };
			if ($@) { push @error, "Error happened: $@\n <em>".$$quote{'id'}."</em>" };
			if ($@ =~ /Error happened:/ && $@ !~/Duplicate entry '\d+?' for key 'PRIMARY'/){ $error = "happened" };
		}
		$sth->finish;
		if($error){ $dbh->disconnect; return @error; };
	}
	1;
}

sub get_new_quote {
	my $ans;
	my $db = shift;
	my $userUid = shift;
	my $readStatus = shift;
	my $error;
	my $sqlQuery = "SELECT * FROM bash WHERE bash.id NOT IN (SELECT quote_id FROM readed WHERE uid = '$userUid' AND readed.key != 0) LIMIT 0, 1;";
	eval { $ans = get_data($db, $sqlQuery); };
	if($@){ return "Error calling function [get_data]: $@\n" };
	if(ref \$ans eq 'SCALAR'){ return "Some DB error: $ans\n" }
	elsif(!$$ans[0][0]){ return "No new quotes." }
	else{
		my $quote_id = $$ans[0][0];
		my $quote = $$ans[0][1];		
		if($readStatus){
			$sqlQuery = "INSERT INTO readed (uid, quote_id, readed.key) VALUES ('$userUid', '$quote_id', 1);";
			eval { $ans = get_data($db, $sqlQuery); };
			if($@){ return "Error calling function [get_data]: $@\n" }
		}
		return [$quote_id, $quote];
	}
}

sub create_uid{
	my $uid = '';
	#my @aArr = ('a'..'z');
	#for my $i ( split '', int(rand(999999)) * int(rand(100500)) + time ){ $uid .= $i*int(rand 10); if(int(rand 2)==1){$uid.=$aArr[int(rand 25)]} };
	for my $i ( split '', int(rand(999999)) * int(rand(100500)) + time ){ $uid .= $i*int(rand 10); if(int(rand 2)==1){$uid .= substr(join('',('a'..'z')), int(rand 25), 1)} };
	return $uid;
}


1;
