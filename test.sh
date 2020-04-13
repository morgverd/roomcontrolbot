r=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)
read -p "To confirm type '$r' >> " check
if test "$check" = "$r"; then
	echo "ay"
else
	echo "Incorrect Confirmation Code"
	exit
fi