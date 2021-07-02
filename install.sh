if ! command -v mania &> /dev/null; then
  printf "Please make sure that mania is properly installed\n"
  exit
fi
printf "Please select\n";
if command -v oboe &> /dev/null; then
  printf "1: Update Oboe\n"
else
  printf "1: Install Oboe\n"
fi
printf "2: Uninstall Oboe\n";
printf "> ";

#Repeat only if the user hasn't entered an integer
while ! [[ $selection =~ ^[1-2]+$ ]];
do
    read selection;
    #if the entered value was not an integer, show this
    if ! [[ $selection =~ ^[1-2]+$ ]]; then
        sleep 1;
        printf "$(tput setaf 9)Please try again$(tput sgr0)\n";
        if command -v oboe &> /dev/null; then
          printf "1: Update Oboe\n"
        else
          printf "1: Install Oboe\n"
        fi
        printf "2: Uninstall Oboe\n";
        printf "> ";
    fi
done

case $selection in
    1)
    #Install
	rm ~/.local/bin/oboe &> /dev/null
	rm ~/.local/share/applications/Oboe.desktop &> /dev/null
	rm ~/.icons/oboe.svg &> /dev/null
	cp oboe.py ~/.local/bin/oboe &> /dev/null
	cp oboe.desktop ~/.local/share/applications/oboe.desktop &> /dev/null
	cp oboe.svg ~/.icons/oboe.svg &> /dev/null
	if command -v oboe &> /dev/null; then
	  printf "Successfully installed Oboe\n"
	elif test -f ~/.local/bin/oboe; then
	  printf "Successfully installed Oboe\nPlease make sure that ~/.local/bin is in your PATH\n"
	else
	  printf "Oboe was not installed\n"
	fi
    ;;

    2)
    #Uninstall
	rm ~/.local/bin/oboe &> /dev/null
	rm ~/.local/share/applications/oboe.desktop &> /dev/null
	rm ~/.icons/oboe.svg &> /dev/null
	if ! test -f ~/.local/bin/oboe; then
	  printf "Successfully uninstalled Oboe\n"
	else
	  printf "Oboe was not uninstalled\n"
	fi
    ;;

    *)
    ;;
esac
