#!/bin/bash

folder=$(find /home /usr /var /tmp /opt /mnt /root -type d -name recon_enum -print -quit 2>/dev/null)
echo -e '#!/bin/bash\n' > /usr/bin/reconscan
echo -e "cd  $folder && python reconscan.py \"\$@\" \n" >> /usr/bin/reconscan
chmod +x /usr/bin/reconscan

