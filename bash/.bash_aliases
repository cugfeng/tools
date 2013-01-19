alias vi=vim
alias vimr='vim -R'

alias findhh='find . -name "*.h" -type f 2>/dev/null'
alias findch='find . -name "*.[ch]" -type f 2>/dev/null'
alias findcc='find . -regex ".*\.\(h\|c\|cpp\)" -type f 2>/dev/null'
alias findpy='find . -name "*.py" -type f 2>/dev/null'
alias findjs='find . -name "*.js" -type f 2>/dev/null'
alias findss='find . -name "*.[sS]" -type f 2>/dev/null'

alias killone='ps -ef | grep ubuntuone | grep -v grep | awk "{print $2}" | xargs sudo kill'
