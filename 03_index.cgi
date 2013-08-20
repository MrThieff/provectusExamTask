#!/usr/bin/perl -w
use strict;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser);
use CGI::Cookie;
use CGI::Session;
#use LWP;
#use myDumper;
use myDBfunc;
#use Data::Dumper;


#print "Content-Type: text/html\n\n";
print <<HTML;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
<title>Login</title>
<style>
	div{margin-bottom: 5px; padding-left: 10px;}
</style>
</head>
<body>
<h1>reader quotes in bash.org.ru</h1>
<p>you can read quotes after login</p>
<!--<a href="03_index.cgi"><h1>Login</h1></a>
<a href="03_page.cgi"><h5>Page</h5></a>-->
HTML

my $login;
my $password;
my $status;
my @error = ();

#print "<div style='background: #e0e0e0; border: solid gray 1px;'>";
#print "<p style='text-align: center;'>WORKING INFORMATION:</p>";

#print "<p>".create_uid()."</p>";

my $query = CGI->new();

my $sid;# = param('sid') || undef;

print header(-expires=>'-1d');

#print $ENV{'HTTP_COOKIE'}."<br/>";
#print $query->param()."<br/>";
#foreach my$i($query->param()){print $i." = ".$query->param($i)."<br/>"};

if( cookie('uid') ){ $status = '+' }

if( $query->param() ){
	$status = '+';
	if($query->param('login')){
		if($query->param('login') =~ /^[a-zA-Z0-9]{4,16}$/){ $login = $query->param('login') }
		else{ push @error, "Incorrect Login. Login can contain 4-16 only alphanummeric simbols." }
	}
	else{ push @error, "Empty Login." }
	if($query->param('password')){
		if($query->param('password') =~ /^[a-zA-Z0-9]{4,16}$/){ $password = $query->param('password') }
		else{ push @error, "Incorrect Password. Password can contain 4-16 only alphanummeric simbols." }
	}
	else{ push @error, "Empty Password." }
}

if($status && !@error){
	my $ans;
	my $sqlQuery = "SELECT * FROM users WHERE login='$login' AND password='$password';";
	if( cookie('uid') ){ $sqlQuery = "SELECT * FROM users WHERE uid='".cookie('uid')."';" }
	eval { $ans = get_data("task63", $sqlQuery); };
	if($@){push @error, "<p>ERROR:\n$@</p>"}
	else{
		if( ref(\$ans) eq 'SCALAR' ){ push @error, "mysql_answer: ".$ans."<br/>" }
		elsif( scalar @$ans == 0 ){ push @error, "The Login or Password is incorrect. Please try again.<br/>" unless cookie('uid') }
		else{
			my $uid = $$ans[0][2];
			if(param('keep_me_signed') eq 'yes'){
				#foreach my $str (@$ans){ print "<p>STR: ".join(" | ", @$str)."\n</p>"; }
				
				#print "<p>".$uid."</p>";
				my $cookie1 = $query->cookie(-name=>'uid',-value=>$uid, -expires=>'3d');
				my $cookie2 = $query->cookie(-name=>'status',-value=>'fv', -expires=>'3d');
				$query->redirect(-location=>'03_page.cgi', -cookie=>[$cookie1, $cookie2] );
			}
			else{
				my $session = new CGI::Session("driver:File", $sid, { Directory => "sessions" });
				$session->name("MYSESSION");
				$session->expire('+1h');
				unless($sid){ $sid = $session->id; $session->param("uid", $uid); }
				my $cookie2 = $query->cookie(-name=>'status',-value=>'fv', -expires=>'3d');
				$query->redirect(-location=>"03_page.cgi?sid=$sid", -cookie=>$cookie2);
				#print "SESSION: ".$session->param("uid")." - ".$session." - ".$sid."<br/>";
				#foreach my $i (%$session){ print $i };
			}
		}
	}
}


#print "</div><br/>";

print <<HTML;
<form method="POST">
	<label for="login">Login:</label>
	<input name="login" type="text" size="30" maxlength="16" value="$login" placeholder="Login"><br/><br/>
	<label for="password">Password:</label>
	<input name="password" type="password" size="30" maxlength="16" value="" placeholder="Password"><br/><br/>
	<label for="checkbox">Keep me signed in: </label>
	<input type="checkbox" name="keep_me_signed" value="yes"><br/><br/>
	<input type="submit" value="LogIn">
</form>
<p style="text-align: right; font-size: 10px; font-style: italic">powered by Dima Mukaeliants</p>
HTML

if(@error){
	print "<div style='background: pink; border: solid red 1px;'>";
	foreach my $error (@error){print "<p>$error</p>"};
	print "</div>";
}

#print "<table width=100% border=1>";
#print qq(<tr><td>$_ </td><td> $ENV{$_}</td><tr>) for sort keys %ENV;
#print "</table>";

print "</body>\n</html>\n";