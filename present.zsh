
if [[ $- == *i* ]]; then

present-next-widget() {
  LBUFFER=$(present --next-and-get)
  zle redisplay
}
zle     -N   present-next-widget
bindkey '^O' present-next-widget

present-prev-widget() {
  LBUFFER=$(present --prev-and-get)
  zle redisplay
}
zle     -N   present-prev-widget
bindkey '^L' present-prev-widget

fi
