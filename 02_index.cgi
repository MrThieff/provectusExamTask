#!/usr/bin/perl -w
use strict;
use CGI;
use CGI::Carp qw(fatalsToBrowser);


print "Content-Type: text/html\n\n";
print <<HTML;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
<title>SendMail</title>
<style>
	div{margin-bottom: 5px; padding-left: 10px;}
</style>
</head>
<body>
<a href="02_index.cgi"><h1>SendMail</h1></a>
HTML

my $sendmail = "/usr/sbin/sendmail -t";
my $to = "To: student\@perlstudent.tm.local\n";
my ($from, $subject, $message) = undef;
my @error = ();
my $status = '';
my @alienCheck = int(rand 2);
if($alienCheck[0] == 1){push @alienCheck, " not"};

my $query = new CGI;

if( $query->param('email') || $query->param('subject') || $query->param('message') ) {
	$status = "not new";
	if( $query->param('email') ){
		if($query->param('email') =~ /[\w\.\-]{1,20}@[\w\-]{1,20}(\.[\w\-]{1,20}){0,4}\.\w{1,10}/){
			$from = $query->param('email');
		}
		else{ push @error, "Please, enter correct e-mail address." };
	}
	else{ push @error, "Enter your Email" };
	if( $query->param('subject') ){$subject = $query->param('subject');}
	else{ push @error, "Enter Subject of email" };
	if( $query->param('message') ){$message = $query->param('message');}
	else{ push @error, "Enter the Message" };
	if( $query->param('alienCheckKey') == 0 && !$query->param('alienCheck') ){ push @error, "You are Alien. Message delivered to NASA. Expect the crew." }
	elsif( $query->param('alienCheckKey') == 1 && $query->param('alienCheck') ){ push @error, "You are Alien. Message delivered to NASA. Expect the crew." }
};

print <<HTML;
<form method="POST">
	<label for="email">Email:</label>
	<input name="email" type="text" size="30" value="$from" placeholder="Email"><br/><br/>
	<label for="subject">Subject:</label>
	<input name="subject" type="text" size="30" value="$subject" placeholder="Subject"><br/><br/>
	<label for="message">Message:</label>
	<textarea name="message" cols="30" rows="10" placeholder="Message">$message</textarea><br/><br/>
	<label for="checkbox">Secret question:</label>
	<input type="checkbox" name="alienCheck" value="yes">\&nbsp;\&nbsp;I'm<em>$alienCheck[1]</em> from the Earth<br/><br/>
	<input type="hidden" name="alienCheckKey" value="$alienCheck[0]">
	<input type="submit" value="Send">
</form>
HTML

if($status){
	if(!@error){
		eval {
			open(SM, "|$sendmail") or die "Cannot open $sendmail: $!";
			print SM "Subject: ".$subject."\n";
			print SM $to;
			print SM "Content-type: text/plain\n\n";
			print SM "From: ".$from."\n";
			print SM $message."\n";
			close(SM);
		};
		if ($@) { push @error, "Error happened: $@\n" }
		else{ $query->redirect("02_index.cgi?sended=OK") }
	}
	if(@error){
		print "<div style='background: pink; border: solid red 1px;'>";
		foreach my $error (@error){print "<p>$error</p>"};
		print "</div>";
	}
}

if($query->param('sended')){
	print "<div style='background: lightgreen; border: solid green 1px;'>";#A2D246
	print "Your e-mail successfully sended.";
	print "</div>";
}

print "</body>\n</html>\n";









