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
  if headings[1] == "Concept" then return nil end
  local output = {}
  for _, body in ipairs(el.bodies) do
    for _, row in ipairs(body.body) do
      output[#output+1] = pandoc.RawBlock("latex", "\\Needspace{7\\baselineskip}\\begin{samepage}")
      for i, cell in ipairs(row.cells) do
        local label = headings[i] or ('Column ' .. i)
        output[#output+1] = pandoc.Para({pandoc.Strong({pandoc.Str(label .. ':')})})
        for _, block in ipairs(cell.contents) do output[#output+1] = block end
      end
      output[#output+1] = pandoc.RawBlock('latex', '\\end{samepage}\\smallskip')
    end
  end
  return output
end

function Para(el)
  if pandoc.utils.stringify(el) == 'Expected output:' then
    return {pandoc.RawBlock('latex', '\\Needspace{9\\baselineskip}'), el}
  end
end

function Header(el)
  if el.level == 2 then
    return {pandoc.RawBlock('latex', '\\Needspace{10\\baselineskip}'), el}
  end
end
