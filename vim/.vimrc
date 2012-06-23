set number
set hlsearch
set cindent
set autoindent
set nocompatible
set wrap
set showmatch
set autochdir

set tabstop=4
set softtabstop=4
set shiftwidth=4
set history=200
set tags=tags;

hi Comment ctermfg=6
filetype plugin on
syntax on

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" cscope setting
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if has("cscope")
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

nmap <F5>s :cs find s <C-R>=expand("<cword>")<CR><CR>
nmap <F5>g :cs find g <C-R>=expand("<cword>")<CR><CR>
nmap <F5>c :cs find c <C-R>=expand("<cword>")<CR><CR>
nmap <F5>t :cs find t <C-R>=expand("<cword>")<CR><CR>
nmap <F5>e :cs find e <C-R>=expand("<cword>")<CR><CR>
nmap <F5>f :cs find f <C-R>=expand("<cfile>")<CR><CR>
nmap <F5>i :cs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
nmap <F5>d :cs find d <C-R>=expand("<cword>")<CR><CR>

nmap <F8>s :%s/<C-R>=expand("<cword>")<CR>///

let g:winManagerWindowLayout = "FileExplorer"
map <c-w><c-t> :WMToggle<cr>
map <c-w><c-f> :TlistToggle<cr>

" disable F1 and map it to Esc
map <F1> <Esc>
imap <F1> <Esc>

let g:LookupFile_TagExpr = string('./filenametags')
let g:alternateNoDefaultAlternate = 1

nnoremap <F2> :set invpaste paste?<CR>
set pastetoggle=<F2>
set showmode

function! ListProjFile()
	let filelist = findfile("cscope.files", ".;")
	if (!empty(filelist))
		exe "e " . filelist
	else
		echo "Warning: no `cscope.files' found!"
	endif
endfunction
function! OpenProjFiles()
	let newfile = getline(line("."))
	if filereadable(newfile)
		exe "e " . newfile
	else
		echo "Warning: no file found!"
	endif
endfunction
nmap <F4>l :call ListProjFile()<CR>
nmap <F4>o :call OpenProjFiles()<CR>
nmap <F4>m :MRU<CR>

