#!/usr/bin/perl -w
use strict;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser);
use CGI::Cookie;
use CGI::Session;
use LWP;
#use myDumper;
use myDBfunc;
#Suse Data::Dumper;
use Encode qw(decode encode);
use utf8;


print <<HTML;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf8"/>
<title>Page</title>
<style>
	div{margin-bottom: 5px; padding: 10px; border: solid black 0px;}
	div div{margin-bottom: 0px; padding: 0px;}
	div form {margin: 0; padding: 0;}
</style>
</head>
<body>
<!--<a href="03_index.cgi"><h1>Login</h1></a>-->
HTML

#print "<div style='background: #e0e0e0; border: solid gray 1px;'>";
#print "<p style='text-align: center;'>WORKING INFORMATION:</p>";
#print "<p>".$ENV{'HTTP_COOKIE'}."</p>";

my @error = ();
my $query = CGI->new();
print header(-charset=>'utf-8');
my $user;
my $cooka = cookie('uid');
my $sid = param('sid') || undef;
my $cookaStatus = cookie('status');
my $postStatus = $query->param('get_new_quote');
my $exitStatus = $query->param('exit');

my $session;
my $uid;
if($sid){
	$session = new CGI::Session("driver:File", $sid, { Directory => "sessions" });
	$session->name("MYSESSION");
	$session->expire('+1h');
	$uid = $session->param("uid");
}
	
#---CHECK USER---#
if($uid || $cooka){
	my $ans;
	my $sqlQuery;
	if($sid){ $sqlQuery = "SELECT * FROM users WHERE uid='$uid';" }
	else{ $sqlQuery = "SELECT * FROM users WHERE uid='$cooka';" }
	
	eval { $ans = get_data("task63", $sqlQuery); };
	if($@){push @error, "<p>get_data: $@</p>"}
	if( ref(\$ans) eq 'SCALAR' ){ push @error, "mysql_answer: ".$ans."<br/>" }
	elsif( scalar @$ans == 0 ){ push @error, "mysql_answer: EMPTY!<br/>" }
	else{
		#foreach my $str (@$ans){ print "<p>STR: ".join(" | ", @$str)."\n</p>"; }
		$user = $$ans[0][0];
		#print "<p>USER: ".$user."</p>";
	}
}

#---UPDATE QUOTES---#
if($user && !@error && ($cookaStatus eq 'fv') ){
	my $url = 'http://bash.im/';
	my $browser = LWP::UserAgent->new;
	my $response = $browser->get( $url );
	unless($response->is_success){ push @error, "Can't get $url -- ", $response->status_line };
	unless($response->content_type eq 'text/html'){ push @error, "Hey, I was expecting HTML, not ", $response->content_type };
	
	my $content = $response->content;
	$content =~ /<div class="quote">/;
	$content = $';
	$content =~ /<div class="pager">/;
	$content = $`;
	Encode::from_to($content, "cp1251", "utf8");
	my @content = split(/<div class="quote">/, $content);
	my @quotes;
	foreach my $elm (@content){
		$elm =~ /<a href\="\/quote\/\d+?" class="id">\#(\d+?)<\/a>/;
		my $currentQuoteID = $1;
		$elm =~ /<div class="text">/;
		my $currentQuote = $';
		$currentQuote =~ s/<\/div>\s*?<\/div>\s*?$//g;
		if($currentQuoteID){ push @quotes, {id=>$currentQuoteID, quote=>$currentQuote} };
	}
	#---send new quotes---#
	my $ans;
	eval { $ans = send_new_quote("task63", \@quotes) };
	if($@){ push @error, "<p>send_new_quote: $@</p>" }
	if( $ans != 1 ){ push @error, "mysql_answer: ".$ans."<br/>" }
	
	#---change cookie Status---#
	my $tempCooka = $query->cookie(-name=>'status',-value=>'');#, -expires => '-1d');
	print header( -cookie=>$tempCooka );
}

#print "</div><br/>";
if($user){
	print "
	<div id='hello_box' style='background: lightgreen; border: solid green 1px;'>
		<div style='text-align: right; width: 50px; float: right;'>
			<form method='POST'>
				<input type='submit' value='Exit'>
				<input type='hidden' name='exit' value='yes'>
				<input type='hidden' name='sid' value='".$sid."'>
			</form>
		</div>
		<div style='width: 200px;'>
			Hello, <em><b>$user</b></em>
		</div>
	</div>";
}
else{ $query->redirect("03_index.cgi") };

#---PRINT QUOTE---#
if($user && !@error){
	my $ans;
	if($postStatus || $exitStatus){ 
		if($cooka){ eval { $ans = get_new_quote("task63", $cooka, 'next') } }
		else{ eval { $ans = get_new_quote("task63", $uid, 'next') } }
		if($@){push @error, "<p>ERROR:\n$@</p>"}
		else{
			if( $query->param('exit') ){
				#---change cookie Status---#
				my $tempCooka = $query->cookie(-name=>'uid',-value=>'');#, -expires => '-1d');
				print header( -cookie=>$tempCooka );
				#$session->clear("uid");
				if($sid){ $session->delete() }
				#undef($session);
				$query->redirect("03_index.cgi");
			}
			else{ $query->redirect("03_page.cgi?sid=$sid") }
		}
	}
	else{
		if($cooka){ eval { $ans = get_new_quote("task63", $cooka) } }
		else{ eval { $ans = get_new_quote("task63", $uid) } }
	}
	if($@){push @error, "<p>ERROR:\n$@</p>"}
	else{
		if($ans =~ /No new quotes./){ print "<div style='text-align: center;'><p>".$ans."</p></div><br/>"; }
		elsif(ref \$ans eq 'SCALAR'){ push @error, "ERROR: ".$ans."" }
		else{
			my $quote_id = $$ans[0];
			my $quote = $$ans[1];
			print "	<div style='text-align: center;'>
						<form method='POST'>
							<input type='submit' value='Next Quote'>
							<input type='hidden' name='get_new_quote' value='yes'>
							<input type='hidden' name='sid' value='".$sid."'>
						</form>
					</div>";
			print "<div style='background: #e0e0e0; border: solid gray 1px;'>";
			print "<p style='text-align: left;'><b>#$quote_id</b></p>";
			print "<p>$quote</p>";
			print "</div><br/>";
		}
	}
}



if(@error){
	print "<div style='background: pink; border: solid red 1px;'>";
	foreach my $error (@error){print "<p>$error</p>"};
	print "</div>";
}

#print "<table width=100% border=1>";
#print qq(<tr><td>$_ </td><td> $ENV{$_}</td><tr>) for sort keys %ENV;
#print "</table>";

print "</body>\n</html>\n";