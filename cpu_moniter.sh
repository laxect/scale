#!/usr/bin/zsh
# a simple shell script for cpu moniter
foo=1
while [ "${foo}" -le 200 ]
do
    # echo $foo
    ps aux | grep scale | grep -v "grep" | grep -v "cpu_moniter"
    sleep 0.1
    # foo=$(($foo+1))
done
exit 0
