set number
set hlsearch
set cindent
set autoindent
set nocompatible
set wrap
set showmatch

set tabstop=4
set softtabstop=4
set shiftwidth=4
set history=200
set tags=tags;

"hi Comment ctermfg=6
filetype plugin on
syntax on

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" cscope setting
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if has("cscope")
	" Mac setting
	" set csprg=/usr/local/bin/cscope
	" Ubuntu setting
	set csprg=/usr/bin/cscope
	set csto=0
	set cst
	set nocsverb
	" add any database in current directory
	if filereadable("cscope.out")
		cs add cscope.out
	" else add database pointed to by environment
	elseif $CSCOPE_DB != ""
		cs add $CSCOPE_DB
	endif
	set csverb
endif
function! LoadCscope()
  let db = findfile("cscope.out", ".;")
  if (!empty(db))
    let path = strpart(db, 0, match(db, "/cscope.out$"))
    set nocscopeverbose " suppress 'duplicate connection' error
    exe "cs add " . db . " " . path
    set cscopeverbose
  endif
endfunction
au BufEnter /* call LoadCscope()

nmap <C-c>s :cs find s <C-R>=expand("<cword>")<CR><CR>
nmap <C-c>g :cs find g <C-R>=expand("<cword>")<CR><CR>
nmap <C-c>c :cs find c <C-R>=expand("<cword>")<CR><CR>
nmap <C-c>t :cs find t <C-R>=expand("<cword>")<CR><CR>
nmap <C-c>e :cs find e <C-R>=expand("<cword>")<CR><CR>
nmap <C-c>f :cs find f <C-R>=expand("<cfile>")<CR><CR>
nmap <C-c>i :cs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
nmap <C-c>d :cs find d <C-R>=expand("<cword>")<CR><CR>

nmap <c-w><c-f> :TlistToggle<CR>
nmap <C-c>o :NERDTree<CR>
nmap <C-c>m :MRU<CR>

" disable F1 and map it to Esc
map <F1> <Esc>
imap <F1> <Esc>

let g:alternateNoDefaultAlternate = 1

nnoremap <F2> :set invpaste paste?<CR>
set pastetoggle=<F2>
set showmode

au BufEnter *.files set cursorline
au BufLeave *.files set nocursorline
au BufEnter * hi Comment ctermfg=6

function! ListProjFile()
	let filelist = findfile("cscope.files", ".;")
	if (!empty(filelist))
		exe "e " . filelist
	else
		echo "Warning: no `cscope.files' found!"
	endif
endfunction
nmap <C-c>l :call ListProjFile()<CR>

