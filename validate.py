"""
Validate the Oireachtas ontology split using rdflib + owlready2.
Parses all local sub-ontologies, resolves owl:imports from the local
ontologies/ directory, and reports classes, properties and individuals.
Also runs the HermiT OWL reasoner (via owlready2) for consistency checking.

Run:  python validate.py

Requires: pip install rdflib owlready2
Also requires Java on PATH (for the bundled HermiT reasoner).
"""
import os
import tempfile
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef
from rdflib.namespace import SKOS

import owlready2
from owlready2 import get_ontology, sync_reasoner

ONTOLOGIES_DIR = Path(__file__).parent / "ontologies"

# Local ontology files to load
ONTOLOGY_FILES = [
    ONTOLOGIES_DIR / "oireachtas.owl.ttl",
    ONTOLOGIES_DIR / "agents.owl.ttl",
    ONTOLOGIES_DIR / "events.owl.ttl",
    ONTOLOGIES_DIR / "legislation.owl.ttl",
    ONTOLOGIES_DIR / "vocabulary.owl.ttl",
    ONTOLOGIES_DIR / "debates.owl.ttl",
    ONTOLOGIES_DIR / "members.owl.ttl",
]

def load_all(paths):
    """Parse all local ontology files into a single merged graph."""
    g = Graph()
    for path in paths:
        print(f"  Parsing {path.name} ...", end=" ")
        try:
            g.parse(str(path), format="turtle")
            print("OK")
        except Exception as e:
            print(f"FAILED: {e}")
    return g

def short(uri):
    """Return the local name of a URI."""
    uri = str(uri)
    return uri.split("#")[-1] if "#" in uri else uri.split("/")[-1]

print("=== Loading ontologies ===")
g = load_all(ONTOLOGY_FILES)
print(f"\nTotal triples loaded: {len(g)}\n")

# --- Classes ---
classes = sorted(
    {s for s in g.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef)},
    key=short
)
print(f"=== OWL Classes ({len(classes)}) ===")
for c in classes:
    label = short(c)
    comment = g.value(c, RDFS.comment)
    print(f"  :{label}" + (f"  — {str(comment)[:80]}" if comment else ""))

# --- Object Properties ---
obj_props = sorted(
    {s for s in g.subjects(RDF.type, OWL.ObjectProperty) if isinstance(s, URIRef)},
    key=short
)
print(f"\n=== Object Properties ({len(obj_props)}) ===")
for p in obj_props:
    domain = g.value(p, RDFS.domain)
    range_ = g.value(p, RDFS.range)
    print(f"  :{short(p)}  domain={short(domain) if domain else '—'}  range={short(range_) if range_ else '—'}")

# --- Data Properties ---
data_props = sorted(
    {s for s in g.subjects(RDF.type, OWL.DatatypeProperty) if isinstance(s, URIRef)},
    key=short
)
print(f"\n=== Data Properties ({len(data_props)}) ===")
for p in data_props:
    print(f"  :{short(p)}")

# --- Named Individuals ---
individuals = sorted(
    {s for s in g.subjects(RDF.type, OWL.NamedIndividual) if isinstance(s, URIRef)},
    key=short
)
print(f"\n=== Named Individuals ({len(individuals)}) ===")
for ind in individuals:
    types = [short(t) for t in g.objects(ind, RDF.type) if t != OWL.NamedIndividual]
    label = g.value(ind, SKOS.prefLabel) or g.value(ind, RDFS.label) or ""
    print(f"  :{short(ind)}  [{', '.join(types)}]" + (f"  \"{label}\"" if label else ""))

# --- SKOS Concept Schemes ---
schemes = sorted(
    {s for s in g.subjects(RDF.type, SKOS.ConceptScheme) if isinstance(s, URIRef)},
    key=short
)
print(f"\n=== SKOS Concept Schemes ({len(schemes)}) ===")
for s in schemes:
    label = g.value(s, SKOS.prefLabel) or ""
    print(f"  :{short(s)}" + (f"  \"{label}\"" if label else ""))

print("\n=== Validation complete (rdflib) ===")

# ---------------------------------------------------------------------------
# Consistency checking with owlready2 + HermiT reasoner
# ---------------------------------------------------------------------------

def run_consistency_check():
    """Load all ontologies via owlready2 and run the HermiT OWL reasoner."""
    print("\n=== Consistency Check (owlready2 + HermiT) ===")

    g_flat = Graph()
    for triple in g:
        if triple[1] != OWL.imports:
            g_flat.add(triple)

    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".owl")
    try:
        with os.fdopen(tmp_fd, "wb") as fh:
            data = g_flat.serialize(format="xml")
            fh.write(data.encode() if isinstance(data, str) else data)

        onto = get_ontology(f"file://{tmp_path}").load()
        print(f"  Loaded merged ontology ({len(list(onto.classes()))} classes) into owlready2.")

        # Run the HermiT DL reasoner (bundled with owlready2; requires Java).
        print("  Running HermiT reasoner (requires Java) …")
        with onto:
            sync_reasoner(infer_property_values=True)

        # sync_reasoner raises OwlReadyInconsistentOntologyError if the
        # ontology is globally inconsistent; reaching here means it is not.
        inconsistent = list(owlready2.default_world.inconsistent_classes())
        if inconsistent:
            print(f"  WARNING — unsatisfiable classes ({len(inconsistent)}):")
            for cls in inconsistent:
                print(f"    - {cls}")
        else:
            print("  RESULT: Ontology is CONSISTENT — no unsatisfiable classes.")

    except owlready2.OwlReadyInconsistentOntologyError:
        print("  RESULT: Ontology is INCONSISTENT (OwlReadyInconsistentOntologyError).")
    finally:
        os.unlink(tmp_path)

run_consistency_check()

