#!/bin/bash


chr() {
  printf \\$(printf '%03o' $1)
}

function hex() {
  printf '%02X\n' $1
}

function encrypt() {
  # essentially, the encrypted message is a xor between msg and reversed(key) (xor pad)
  key=$1
  msg=$2
  crpt_msg=""
  for ((i=0; i<${#msg}; i++)); do
    c=${msg:$i:1} # get ith char
    asc_chr=$(echo -ne "$c" | od -An -tuC) # get decimal representation of c
    key_pos=$((${#key} - 1 - ${i})) # compute len(key)-i-1 (ith index for key from the right)
    key_char=${key:$key_pos:1} # get key[key_pos]
    crpt_chr=$(( $asc_chr ^ ${key_char} )) # xor between msg[i] and key[-i] (assumes key[-i] is going to be a number!)
    hx_crpt_chr=$(hex $crpt_chr) # transform to hex
    crpt_msg=${crpt_msg}${hx_crpt_chr} # append to end
  done
  echo $crpt_msg
}

function decrypt() {
  # with a bit of tweaking, decrypting is essentially the same as encrypting
  key=$1
  cyphertext=$2
  decrypted_msg=""
  for ((i=0; i<${#cyphertext}; i += 2)); do
    chr_dec=$((16#${cyphertext:$i:2}))
    key_pos=$((${#key} - 1 - $i/2))
    key_char=${key:$key_pos:1}
    dcrp_chr=$(chr $(( $chr_dec ^ $key_char )))
    decrypted_msg=${decrypted_msg}${dcrp_chr}
  done
  echo $decrypted_msg
}

function break_key() {
  msg=$1
  cyphertext=$2
  key=""
  for ((i=0; i<${#cyphertext}; i += 2)); do
    msg_pos=$(( i / 2 ))
    c=${msg:$msg_pos:1}
    asc_chr=$(echo -ne "$c" | od -An -tuC)
    crypt_chr=$((16#${cyphertext:$i:2}))
    key_digit=$(( $asc_chr ^ $crypt_chr ))
    key=${key_digit}${key}
  done
  echo $key
}


MSG1="514;248;980;347;145;332"
CYPHERTEXT1="3633363A33353B393038383C363236333635313A353336"
CYPHERTEXT2="3A3A333A333137393D39313C3C3634333431353A37363D"


key=$(break_key $MSG1 $CYPHERTEXT1)
echo "The key is $key"

MSG2=$(decrypt $key $CYPHERTEXT2)
echo "The coordinates are $MSG2"
echo $MSG2 > output


