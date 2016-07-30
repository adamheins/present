
if [[ $- == *i* ]]; then

present-next-widget() {
  present --next
  LBUFFER=$(present --get)
  zle redisplay
}
zle     -N   present-next-widget
bindkey '^O' present-next-widget

present-prev-widget() {
  present --prev
  LBUFFER=$(present --get)
  zle redisplay
}
zle     -N   present-prev-widget
bindkey '^L' present-prev-widget

fi
