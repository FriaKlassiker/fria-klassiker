-- Stephanus-sidor: [43]{.steph} blir marginalsiffra i PDF, flytande siffra i HTML/EPUB (via CSS).
function Span(el)
  if el.classes:includes('steph') and FORMAT:match('latex') then
    local n = pandoc.utils.stringify(el)
    return pandoc.RawInline('latex', '\\steph{' .. n .. '}')
  end
  if el.classes:includes('gr') and FORMAT:match('latex') then
    return {pandoc.RawInline('latex', '{\\grfont '), pandoc.Span(el.content), pandoc.RawInline('latex', '}')}
  end
end

-- Onumrerade kapitel i PDF blir \addchap så att löprubriken följer med.
function Header(el)
  if FORMAT:match('latex') and el.level == 1 and el.classes:includes('unnumbered') then
    local t = pandoc.write(pandoc.Pandoc({pandoc.Plain(el.content)}), 'latex')
    local lab = el.identifier ~= '' and ('\\label{' .. el.identifier .. '}') or ''
    return pandoc.RawBlock('latex', '\\addchap{' .. t .. '}' .. lab)
  end
end

-- Fragmentposter i PDF
local function spanlatex(el, fore, efter)
  local inner = pandoc.write(pandoc.Pandoc({pandoc.Plain(el.content)}), 'latex')
  return pandoc.RawInline('latex', fore .. inner .. efter)
end
local orig_span = Span
function Span(el)
  if FORMAT:match('latex') then
    if el.classes:includes('postref') then return spanlatex(el, '\\postref{', '}') end
    if el.classes:includes('not') then return spanlatex(el, '\\postnot{', '}') end
    if el.classes:includes('kalla') then return spanlatex(el, '\\postkalla{', '}') end
  end
  return orig_span(el)
end

function Div(el)
  if FORMAT:match('latex') and el.classes:includes('post') then
    table.insert(el.content, 1, pandoc.RawBlock('latex', '\\begingroup\\setlength{\\parindent}{0pt}\\setlength{\\parskip}{2pt}'))
    table.insert(el.content, pandoc.RawBlock('latex', '\\endgroup'))
    return el
  end
end
