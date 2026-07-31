const state = { rows: [], stats: {}, filtered: [] };
const filterIds = ["query", "year", "specification", "representation", "allocation", "placement", "guarantee", "evidence", "study_type"];
const ids = [...filterIds, "sort"];
const controls = Object.fromEntries(ids.map((id) => [id, document.getElementById(id)]));

const pretty = (value) => value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
const uniq = (values) => [...new Set(values)].sort((a, b) => String(b).localeCompare(String(a)));

function populate(select, values) {
  for (const value of values) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = pretty(String(value));
    select.append(option);
  }
}

function setStats() {
  document.getElementById("stat-records").textContent = state.stats.records;
  document.getElementById("stat-peer").textContent = state.stats.peer_reviewed;
  document.getElementById("stat-reviewed").textContent = state.stats.full_text_reviewed;
  document.getElementById("stat-code").textContent = state.stats.with_code;
}

function makeTag(value) {
  const span = document.createElement("span");
  span.className = "tag";
  span.textContent = value;
  return span;
}

function makeCard(row) {
  const article = document.createElement("article");
  article.className = "paper-card";

  const top = document.createElement("div");
  top.className = "paper-top";
  const venue = document.createElement("span");
  venue.textContent = `${row.venue} · ${row.year}`;
  const status = document.createElement("span");
  status.className = `status ${row.review_status}`;
  status.textContent = pretty(row.review_status);
  top.append(venue, status);

  const heading = document.createElement("h3");
  const title = document.createElement("a");
  title.href = row.url;
  title.target = "_blank";
  title.rel = "noreferrer";
  title.textContent = row.title;
  heading.append(title);

  const authors = document.createElement("p");
  authors.className = "authors";
  const shown = row.authors.slice(0, 5);
  authors.textContent = shown.join(", ") + (row.authors.length > shown.length ? ` +${row.authors.length - shown.length}` : "");

  const tags = document.createElement("div");
  tags.className = "tags";
  [...row.specification, ...row.placement, ...row.allocation].slice(0, 8).forEach((tag) => tags.append(makeTag(tag)));

  const evidence = document.createElement("p");
  evidence.className = "evidence";
  evidence.textContent = row.evidence_note;

  const links = document.createElement("div");
  links.className = "card-links";
  const paper = document.createElement("a");
  paper.href = row.url;
  paper.target = "_blank";
  paper.rel = "noreferrer";
  paper.textContent = "Paper ↗";
  links.append(paper);
  if (row.code_url) {
    const code = document.createElement("a");
    code.href = row.code_url;
    code.target = "_blank";
    code.rel = "noreferrer";
    code.textContent = "Code ↗";
    links.append(code);
  }

  article.append(top, heading, authors, tags, evidence, links);
  return article;
}

function matches(row) {
  const query = controls.query.value.trim().toLowerCase();
  const haystack = [row.title, row.venue, row.authors.join(" "), row.study_type.join(" "), row.specification.join(" "), row.representation.join(" "), row.allocation.join(" "), row.guarantees.join(" ")].join(" ").toLowerCase();
  return (!query || haystack.includes(query))
    && (!controls.year.value || String(row.year) === controls.year.value)
    && (!controls.specification.value || row.specification.includes(controls.specification.value))
    && (!controls.representation.value || row.representation.includes(controls.representation.value))
    && (!controls.allocation.value || row.allocation.includes(controls.allocation.value))
    && (!controls.placement.value || row.placement.includes(controls.placement.value))
    && (!controls.guarantee.value || row.guarantees.includes(controls.guarantee.value))
    && (!controls.evidence.value || row.review_status === controls.evidence.value)
    && (!controls.study_type.value || row.study_type.includes(controls.study_type.value));
}

function syncUrl() {
  const params = new URLSearchParams();
  for (const id of filterIds) if (controls[id].value) params.set(id, controls[id].value);
  if (controls.sort.value !== "newest") params.set("sort", controls.sort.value);
  history.replaceState(null, "", `${location.pathname}${params.size ? `?${params}` : ""}${location.hash}`);
}

function render() {
  const evidenceRank = { second_pass_verified: 4, full_text_coded: 3, full_text_screened: 2, metadata_verified: 1 };
  const comparators = {
    newest: (a, b) => b.year - a.year || a.title.localeCompare(b.title),
    oldest: (a, b) => a.year - b.year || a.title.localeCompare(b.title),
    title: (a, b) => a.title.localeCompare(b.title),
    evidence: (a, b) => evidenceRank[b.review_status] - evidenceRank[a.review_status] || b.year - a.year || a.title.localeCompare(b.title),
  };
  state.filtered = state.rows.filter(matches).sort(comparators[controls.sort.value]);
  const grid = document.getElementById("paper-grid");
  grid.replaceChildren(...state.filtered.map(makeCard));
  document.getElementById("result-count").textContent = `${state.filtered.length} of ${state.rows.length} records`;
  const active = filterIds.filter((id) => controls[id].value).map((id) => `${pretty(id)}: ${pretty(controls[id].value)}`);
  document.getElementById("active-summary").textContent = active.join(" · ");
  document.getElementById("empty").hidden = state.filtered.length !== 0;
  syncUrl();
}

function reset() {
  filterIds.forEach((id) => { controls[id].value = ""; });
  controls.sort.value = "newest";
  render();
}

function chart(id, counts) {
  const root = document.getElementById(id);
  const entries = Object.entries(counts).filter(([key]) => key !== "not_reported").sort((a, b) => b[1] - a[1]).slice(0, 8);
  const max = Math.max(...entries.map(([, value]) => value), 1);
  for (const [label, count] of entries) {
    const row = document.createElement("div"); row.className = "bar-row";
    const name = document.createElement("span"); name.className = "bar-label"; name.textContent = pretty(label);
    const track = document.createElement("div"); track.className = "bar-track";
    const fill = document.createElement("div"); fill.className = "bar-fill"; fill.style.width = `${100 * count / max}%`; track.append(fill);
    const value = document.createElement("span"); value.className = "bar-count"; value.textContent = count;
    row.append(name, track, value); root.append(row);
  }
}

async function init() {
  try {
    [state.rows, state.stats] = await Promise.all([
      fetch("catalog.json").then((response) => response.json()),
      fetch("stats.json").then((response) => response.json()),
    ]);
    setStats();
    populate(controls.year, uniq(state.rows.map((row) => String(row.year))));
    populate(controls.specification, uniq(state.rows.flatMap((row) => row.specification)));
    populate(controls.representation, uniq(state.rows.flatMap((row) => row.representation)));
    populate(controls.allocation, uniq(state.rows.flatMap((row) => row.allocation)));
    populate(controls.placement, uniq(state.rows.flatMap((row) => row.placement)));
    populate(controls.guarantee, uniq(state.rows.flatMap((row) => row.guarantees).filter((value) => value !== "not_reported")));
    populate(controls.evidence, uniq(state.rows.map((row) => row.review_status)));
    populate(controls.study_type, uniq(state.rows.flatMap((row) => row.study_type)));

    const params = new URLSearchParams(location.search);
    ids.forEach((id) => { if (params.has(id)) controls[id].value = params.get(id); });
    ids.forEach((id) => controls[id].addEventListener(id === "query" ? "input" : "change", render));
    document.getElementById("reset").addEventListener("click", reset);
    document.querySelector("#empty button").addEventListener("click", reset);

    chart("chart-specification", state.stats.specification);
    chart("chart-placement", state.stats.placement);
    chart("chart-guarantees", state.stats.guarantees);
    chart("chart-systems", state.stats.systems_measurements);
    render();
  } catch (error) {
    document.getElementById("result-count").textContent = "Catalog failed to load";
    console.error(error);
  }
}

init();
