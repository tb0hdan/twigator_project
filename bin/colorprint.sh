#!/bin/bash

# TODO: Use all available colors
# https://misc.flogisoft.com/bash/tip_colors_and_formatting
color=$1
TEMPLATE_GREEN="\033[1;32m"
TEMPLATE_RED="\033[1;31m"
TEMPLATE_OFF="\033[0m"
case ${color} in
    green)
        template=${TEMPLATE_GREEN}
        ;;
    red)
        template=${TEMPLATE_RED}
        ;;
    off)
        template=${TEMPLATE_OFF}
        ;;
    *)
        template=${TEMPLATE_OFF}
        ;;
esac

shift
if [ "$TERM" == "xterm-256color" ]; then
    printf ${template}$*${TEMPLATE_OFF}
else
    printf $*
fi
