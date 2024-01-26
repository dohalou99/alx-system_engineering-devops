# Increase hard file limit for holberton user
file { 'loginFile':
    ensure  => present,
    path    => '/etc/security/limits.conf',
    content => '#File erased'
}
