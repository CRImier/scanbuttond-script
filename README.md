This is Python script to use with scanbuttond for easy one-button scanning. It has logging, analysing exit codes of programs used to determine when things go wrong and sound notifications. Unfortunately, it doesn't support determining which scanner button was pressed (wasn't needed for me), but you can add this, you know =)
It depends on scanimage and imagemagick. Is to be used with pybssort, the program I (CRImier) have in my GitHub Gists. Pybssort is used to determine scanning directory, so its usage can be avoided by hard-coding the directory.
Also, I kind of like the code I wrote =) Seems clear and so I'm not afraid of putting it here where others can see it. Also, I hope it would be easy to modify this.
I'm currently unable to find where I found those two sounds included from, but I remember they were in some sound library licensed under CC or such. After some time I'll probably add sound licensing information =) 
User that scanbuttond runs under has to be in groups "scanner" and "audio".
All the files have to be put in /etc/scanbuttond/ directory.
Script depends on scanimage (sane-utils), convert (imagemagick), aplay (alsa-utils) and pybssort (https://gist.github.com/CRImier/7330722) 

Feel free to contact me on crimier@yandex.ru if something's wrong.
