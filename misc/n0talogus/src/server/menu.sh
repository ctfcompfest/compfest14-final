#!/bin/bash
set -o history
set -o histexpand
set -o braceexpand

cat nothingtosee.txt
echo "Starting Process..."
echo secret/do/you/wonder/what/is/inside/this/well/then,/let/me/show/you/not_your_flag3
for i in {1..10}
do
  echo "$i"
  sleep .3
done
echo secret/do/you/wonder/what/is/inside/this/well/then,/let/me/show/you/not_your_flag2
echo secret/do/you/wonder/what/is/inside/this/well/then,/let/me/show/you/not_your_flag
echo -e "Process Started\n\n"

sleep .5
echo "========================================================================================================" 
echo "###########################                     MAIN MENU                    ###########################"
echo "========================================================================================================" 

sleep .2
echo -e "\n Here's a part of the script.\n"
sleep .2

echo -e  '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
cat ./main.txt
echo -e  '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

sleep 1

whitelist=("'" "p" "0" "4" "y" "1" "t" "2" ":" "7" "h" "6" "r" "3" "s" ";" "5" "o" "-"  "8" "i" "9" "!" " ")

function finish_program(){
sleep .5
echo -e "\ninteraction finished"
echo "exiting program..."
sleep .2
}

echo -e "\nWelcome! I can only grant you one wish. be careful of what you wish for."
read -p "What is your wish? : " input
counter=0
input=${input//$'\n'/}

for (( i=0; i<${#input}; i++ )); do
  if ! [[ "${whitelist[*]}" =~ ${input:$i:1} ]]
  then
    ((counter++))
  fi
done

if [[ "$counter" -gt 0 ]]
then
 echo "What Are you Doing?!"
else
 eval "eval \$\($input\)" 2>/dev/null || eval $input 2>/dev/null || echo "failed"
fi

finish_program

echo -e "\n========================================================================================================"
echo "#########################                     END OF PROGRAM                   #########################"
echo "========================================================================================================" 

source ./cleaner.sh
