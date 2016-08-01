
if [[ $- == *i* ]]; then

present-next-widget() {
  text=$(present --next-and-get)
  if [[ $text[1] == ">" ]]; then
    echo ""
    echo $text[2,-1]
  else
    LBUFFER="$text"
    zle redisplay
  fi
}
zle     -N   present-next-widget
bindkey '^O' present-next-widget

present-prev-widget() {
  text=$(present --prev-and-get)
  if [[ $text[1] != ">" ]]; then
    LBUFFER="$text"
    zle redisplay
  fi
}
zle     -N   present-prev-widget
bindkey '^L' present-prev-widget

fi
