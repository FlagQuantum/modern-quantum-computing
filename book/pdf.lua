-- Pair mathematical statements with their implementations in print.
local equation = 0
function Math(el)
  if el.mathtype == 'DisplayMath' then
    equation = equation + 1
    return pandoc.RawInline('latex', '\\begin{equation}\\label{eq:print-' .. equation .. '}\n' .. el.text .. '\n\\end{equation}')
  end
end
local function celltex(cell)
  local blocks = pandoc.walk_block(pandoc.Div(cell.contents), {
    Code = function(code)
      return pandoc.RawInline('latex', '\\lstinline|' .. code.text .. '|')
    end
  }).content
  return pandoc.write(pandoc.Pandoc(blocks), 'latex')
end
function Table(el)
  local head = el.head.rows[1]
  if not head or #head.cells ~= 2 or pandoc.utils.stringify(head.cells[1].contents) == 'Concept' then return nil end
  local output = {}
  local first = true
  local labels = {'FORMULA / OPERATION', 'FLAGQUANTUM / PYTORCH'}
  for _, body in ipairs(el.bodies) do
    for _, row in ipairs(body.body) do
      local tex = '\\Needspace{5\\baselineskip}\\par\\noindent\n'
      for i, cell in ipairs(row.cells) do
        local width = i == 1 and '0.40' or '0.56'
        tex = tex .. '\\begin{minipage}[t]{' .. width .. '\\linewidth}\\vspace{0pt}\\raggedright\n'
        if first then tex = tex .. '{\\sffamily\\footnotesize\\bfseries\\color{bookteal}' .. labels[i] .. '}\\par\\smallskip\n' end
        tex = tex .. celltex(cell) .. '\n\\end{minipage}'
        if i == 1 then tex = tex .. '\\hfill\n' end
      end
      tex = tex .. '\\par\\nobreak\\vspace{0.35em}{\\color{codebackground}\\hrule height 0.7pt}\\vspace{0.5em}\n'
      output[#output+1] = pandoc.RawBlock('latex', tex)
      first = false
    end
  end
  return output
end
function Para(el)
  if pandoc.utils.stringify(el):match('^Implementation excerpt') then
    return {pandoc.RawBlock('latex', '\\Needspace{12\\baselineskip}'), el}
  end
  if pandoc.utils.stringify(el) == 'Expected output:' then
    return {pandoc.RawBlock('latex', '\\Needspace{5\\baselineskip}'), el}
  end
end

function Header(el)
  if el.level == 2 and pandoc.utils.stringify(el) == 'Run and verify' then
    return {pandoc.RawBlock('latex', '\\Needspace{14\\baselineskip}'), el}
  end
end

function CodeBlock(el)
  -- Keep short programs and excerpts intact; long listings may still paginate.
  local lines = 0
  for line in (el.text .. '\n'):gmatch('(.-)\n') do
    lines = lines + math.max(1, math.ceil(#line / 86))
  end
  if lines <= 42 then
    return {pandoc.RawBlock('latex', '\\Needspace{' .. (lines * 13 + 24) .. 'pt}'), el}
  end
end
