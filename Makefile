### Makefile --- 

## Author: shell@Shell-MBPT-SH.local
## Version: $Id: Makefile,v 0.0 2019/04/09 08:12:49 shell Exp $
## Keywords: 
## X-URL: 

# refer: https://scripttiger.github.io/macs/

build:
	curl -sS 'https://scripttiger.github.io/macs/data/simplified.txt' | python macs.py -c | gzip > ouis.gz


### Makefile ends here
