#!/bin/bash

clear

function color (){
  echo "\e[$1m$2\e[0m"
}

function extend (){
  local str="$1"
  let spaces=60-${#1}
  while [ $spaces -gt 0 ]; do
    str="$str "
    let spaces=spaces-1
  done
  echo "$str"
}

function center (){
  local str="$1"
  let spacesLeft=(78-${#1})/2
  let spacesRight=78-spacesLeft-${#1}
  while [ $spacesLeft -gt 0 ]; do
    str=" $str"
    let spacesLeft=spacesLeft-1
  done

  while [ $spacesRight -gt 0 ]; do
    str="$str "
    let spacesRight=spacesRight-1
  done

  echo "$str"
}

function sec2time (){
  local input=$1

  if [ $input -lt 60 ]; then
    echo "$input seconds"
  else
    ((days=input/86400))
    ((input=input%86400))
    ((hours=input/3600))
    ((input=input%3600))
    ((mins=input/60))

    local daysPlural="s"
    local hoursPlural="s"
    local minsPlural="s"

    if [ $days -eq 1 ]; then
      daysPlural=""
    fi

    if [ $hours -eq 1 ]; then
      hoursPlural=""
    fi

    if [ $mins -eq 1 ]; then
      minsPlural=""
    fi

    echo "$days day$daysPlural, $hours hour$hoursPlural, $mins minute$minsPlural"
  fi
}



headerHassColor=36
greetingsColor=32
statsLabelColor=33

# Header
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,,,,,,,,,,,,, ,,,,,,,,,,,,,,,,,,,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,,,,,,,,,,,,   ,,,,,,,,,,,,,,,,,,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,,,,,,,,,,,     ,,,,,,,,,,,,,,,,,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,,,,,,,,,,       ,,,,,,,,,,,,,,,,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,,,,,,,,,         ,,,,,,,,,,,,,,,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,,,,,,,,           ,,,,,,,,,,,,,,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,,,,,,,             ,,,,,,,,,,,,,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,,,,,,               ,,,,,,,,,,,,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,,,,,       ,,,,.     ,,,,,,,,,,,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,,,,       ,,,,,,,     ,,,,,,,,,,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,,,       ,,,,,,,,,     ,,,     ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,,        ,,,   ,,,      ,,     ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,         ,,,   ,,,       ,     ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,          ,,,   ,,,             ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,            ,,,,,,,              ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,              ,,,,,               ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,                ,,,                ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,                 ,,,                 ,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,        ,,,       ,,,       ,,,        ,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,       ,,,,,,,     ,,,     ,,,,,,,       ,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,       ,,,,,,,,,    ,,,    ,,,,,,,,,       ,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,        ,,,   ,,,    ,,,    ,,,   ,,,        ,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,         ,,,   ,,,    ,,,    ,,,   ,,,         ,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,   ,,,   ,,,    ,,,    ,,,   ,,,   ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,    ,,,,,,,,    ,,,    ,,,,,,,,    ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,      ,,,,,,    ,,,    ,,,,,,      ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,        ,,,,,   ,,,   ,,,,,        ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,          ,,,,  ,,,  ,,,,          ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,           ,,,, ,,, ,,,,           ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,            ,,,,,,,,,,,            ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,             ,,,,,,,,,             ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,              ,,,,,,,              ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,               ,,,,,               ,,,,,,,,,,")\n"
header="$header$(color $headerHassColor ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")\n"


me=$(whoami)

# Greetings
greetings="$greetings$(color $greetingsColor "$(date +"%A, %d %B %Y, %T")")\n\n"
greetings="$(color $greetingsColor "Home Assistant config files are located in: /home/hass")\n"




uptime="$(sec2time $(cut -d "." -f 1 /proc/uptime))"
uptime="$uptime ($(date -d "@"$(grep btime /proc/stat | cut -d " " -f 2) +"%d-%m-%Y %H:%M:%S"))"

label2="$(extend "$uptime")"
label2="$(color $statsLabelColor "Uptime........:") $label2"

label3="$(extend "$(free -m | awk 'NR==2 { printf "Total: %sMB, Used: %sMB, Free: %sMB",$2,$3,$4; }')")"
label3="$(color $statsLabelColor "Memory........:") $label3"

label4="$(extend "$(df -h ~ | awk 'NR==2 { printf "Total: %sB, Used: %sB, Free: %sB",$2,$3,$4; }')")"
label4="$(color $statsLabelColor "Home space....:") $label4"


stats="$label1\n$label2\n$label3\n$label4\n$label5"

# Print motd
echo -e "$header\n$greetings\n$stats\n"    
