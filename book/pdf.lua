-- PDF-specific presentation; the Markdown remains the canonical chapter source.
local equation = 0
function Math(el)
  if el.mathtype == 'DisplayMath' then
    equation = equation + 1
    return pandoc.RawInline('latex', '\\begin{equation}\\label{eq:print-' .. equation .. '}\n' .. el.text .. '\n\\end{equation}')
  end
end
function Table(el)
  -- Narrow print pages cannot hold formula/code tables comfortably.
  -- Keep each row as a consecutive labeled correspondence block instead.
  local headings = {}
  local head = el.head.rows[1]
  if head then
    for _, cell in ipairs(head.cells) do
      headings[#headings+1] = pandoc.utils.stringify(cell.contents)
    end
  end
  local output = {}
  for _, body in ipairs(el.bodies) do
    for _, row in ipairs(body.body) do
      for i, cell in ipairs(row.cells) do
        local label = headings[i] or ('Column ' .. i)
        output[#output+1] = pandoc.Para({pandoc.Strong({pandoc.Str(label .. ':')})})
        for _, block in ipairs(cell.contents) do output[#output+1] = block end
      end
      output[#output+1] = pandoc.RawBlock('latex', '\\medskip')
    end
  end
  return output
end
